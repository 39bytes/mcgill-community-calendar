import os
from flask import (Blueprint, request, url_for, redirect, render_template, flash, g, abort, current_app)
from community_calendar.models import Event
from community_calendar import auth
from community_calendar.database import db_session
from sqlalchemy import exc
from datetime import datetime, timedelta
from typing import List
from community_calendar.models import VALID_TAGS
from community_calendar.utils import allowed_file, append_timestamp_and_hash

bp = Blueprint('event', __name__)

@bp.route('/')
def index():
    filtered_tags = request.args.get("filtered_tags")

    if filtered_tags is None:
        filtered_tags = ""

    page = request.args.get("page")
    if page is None:
        page = 0
    page = int(page)

    tags_list = filtered_tags.split(",")
    start_date = datetime.now() + timedelta(days=14*page)

    offset = start_date.isoweekday() % 7 # Sunday = 0, Monday = 1, ... Saturday = 6
    start_date = start_date - timedelta(days=offset)
    events = Event.query.filter(Event.start_time < start_date + timedelta(days=14)) \
                        .filter(Event.start_time > start_date) \
                        .order_by(Event.start_time).all()

    # Gets events where tags with any of the filtered tags
    events = [event for event in events if any(tag in event.tags for tag in tags_list)]
    events = group_by_day(events, start_date)
    return render_template('event/index.html', 
            filtered_tags=filtered_tags, valid_tags=VALID_TAGS, events=events,
            offset=timedelta(days=offset), current_day=start_date)

@bp.route("/<int:id>/info", methods=("GET",))
def info(id):
    event = Event.query.filter(Event.id == id).first()
    if event is None:
        abort(404)
    return render_template("event/info.html", event=event)


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@auth.login_required
def edit(id):
    error = None
    event = Event.query.filter(Event.id == id).first()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        start_time = request.form["start_time"]
        tags = request.form.getlist('tags[]')
        
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

        if datetime.now() > start_time:
            error = "Start time must be in the future."

        if error is None:

            new_image = request.files["eventImage"]
            new_filename = event.image_filename

            if new_image:
                if event.image_filename:
                    filename = event.image_filename
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                new_filename = append_timestamp_and_hash(new_image.filename)
                new_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))

            setattr(event, "name", name)
            setattr(event, "description", description)
            setattr(event, "location", location)
            setattr(event, "start_time", start_time)
            setattr(event, "image_filename", new_filename)
            setattr(event, "tags", ",".join(tags))
            db_session.commit()

            return redirect(url_for("event.info", id=event.id))

        flash(error)

    return render_template("event/edit.html", event=event, valid_tags=VALID_TAGS)

@bp.route("/create", methods=("GET", "POST"))
@auth.login_required
def create():
    if request.method == "POST":
        name = request.form['name']
        location = request.form['location']
        start_time = request.form['start_time']
        description = request.form['description']
        tags = request.form.getlist('tags[]')
        image = request.files['eventImage']
        error = None

        if not name:
            error = "A name is required."
        elif not location:
            error = "A location is required"
        elif not start_time:
            error = "A start time is required"
        elif not description:
            error = "A description is required"

        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

        if datetime.now() > start_time:
            error = "Start time must be in the future."

        if error is None:
            try:
                filename = ''
                if image and allowed_file(image.filename):
                    filename = append_timestamp_and_hash(image.filename)
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                event = Event(name, g.user.id, description, location, start_time, ",".join(tags), filename)
                db_session.add(event)
                db_session.commit()
            except exc.IntegrityError:
                db_session.rollback()
                if filename:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                error = f"An event with those details already exists!"
            else:
                return redirect(url_for("event.info", id=event.id))

        flash(error)

    return render_template('event/create.html', valid_tags=VALID_TAGS)

@bp.route('/<int:id>/delete', methods=("POST",))
@auth.login_required
def delete(id):
    Event.query.filter(Event.id == id).delete()
    db_session.commit()
    return redirect(url_for("index"))

def group_by_day(events: List[Event], start_day):
    """Takes a list of events ordered by start time, and groups them by day."""
    if not events:
        return []

    grouped = []

    current_day = start_day
    current_day_events = []
    for event in events:
        # Event on same day
        if (current_day.year == event.start_time.year 
            and current_day.month == event.start_time.month 
            and current_day.day == event.start_time.day):
            current_day_events.append(event)
        else:
            # Event on new day
            grouped.append(current_day_events)
            diff = event.start_time.day - current_day.day
            for i in range(diff - 1):
                grouped.append([])
            current_day = event.start_time
            current_day_events = [event]
    grouped.append(current_day_events)
    grouped += [[]] * (14 - len(grouped))
    return grouped

@bp.app_template_filter()
def add_days(date: datetime, days: int):
    return date + timedelta(days=days)
    
@bp.app_template_filter()
def str_strip(s : str, strip_char: str):
    return s.strip(strip_char)
    