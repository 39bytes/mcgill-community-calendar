import os
from flask import (Blueprint, request, url_for, redirect, render_template, flash, g, abort, current_app)
from codejamapp.models import Event
from codejamapp import auth
from codejamapp.database import db_session
from sqlalchemy import exc
from datetime import datetime, timedelta
from typing import List
from codejamapp.models import VALID_TAGS
from codejamapp.utils import allowed_file, append_timestamp_and_hash

bp = Blueprint('event', __name__)

@bp.route('/')
def index():
    filtered_tags = request.args.get("filtered_tags")
    if filtered_tags is None:
        filtered_tags = ""
    tags_list = filtered_tags.split(",")
    now = datetime.now()
    
    offset = now.isoweekday() % 7 # Sunday = 0, Monday = 1, ... Saturday = 6
    events = Event.query.filter(Event.start_time < now + timedelta(days=14-offset)) \
                        .filter(Event.start_time > now - timedelta(days=offset)) \
                        .order_by(Event.start_time).all()

    # Gets events where tags with any of the filtered tags
    events = [event for event in events if any(tag in event.tags for tag in tags_list)]
    events = group_by_day(events, now - timedelta(days=offset))
    print(VALID_TAGS)
    return render_template('event/index.html', 
            filtered_tags=filtered_tags, valid_tags=VALID_TAGS, events=events, 
            offset=timedelta(days=offset), current_day=now)

@bp.route("/<int:id>/info", methods=("GET",))
def info(id):
    event = Event.query.filter(Event.id == id).first()
    if event is None:
        abort(404)
    return render_template("event/info.html", event=event)


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@auth.login_required
def edit(id):
    event = Event.query.filter(Event.id == id).first()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        start_time = request.form["start_time"]
        
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

        setattr(event, "name", name)
        setattr(event, "description", description)
        setattr(event, "location", location)
        setattr(event, "start_time", start_time)
        db_session.commit()

        return redirect(url_for("event.info", id=event.id))

    return render_template("event/edit.html", event=event)
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

        print(tags)

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

    return render_template('event/create.html')

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
    