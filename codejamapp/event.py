from flask import (Blueprint, request, url_for, redirect, render_template, flash, g, abort)
from codejamapp.models import Event, User
from codejamapp import auth
from codejamapp.database import db_session
from sqlalchemy import exc
from datetime import datetime

bp = Blueprint('event', __name__, url_prefix="/event")

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
        # update event
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

        if error is None:
            try:
                event = Event(name, g.user.id, description, location, start_time)
                db_session.add(event)
                db_session.commit()
            except exc.IntegrityError:
                db_session.rollback()
                error = f"An event with those details already exists!"
            else:
                return redirect(url_for("event.info", id=event.id))

            flash(error)

    return render_template('event/create.html')


