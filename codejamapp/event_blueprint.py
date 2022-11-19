from flask import (Blueprint, request, url_for, redirect, render_template, flash)
from codejamapp.models import Event, User
from codejamapp import auth
from codejamapp.database import db_session
from sqlalchemy import exc

bp = Blueprint('event_blueprint', __name__, url_prefix="/event")

@bp.route(Event.id, methods=("GET",))
@auth.login_required()
def display_event():
    if request.method == "GET":
        event = Event.query.filter(Event.id == id).first()
        if event is not None:
            return render_template(Event.id)
    return redirect(url_for("index"))


@bp.route(Event.id, methods=("GET", "POST"))
@auth.login_required()
def edit_event():
    event = Event.query.filter(Event.id == id).first()
    if request.method == "POST":
        event.update()
        return render_template(Event.id)
    return redirect(url_for("index"))

@bp.route(Event.id, methods=("GET", "POST"))
@auth.login_required()
def create_event():
    name = request.form['name']
    location = request.form['location']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    error = None

    if not name:
        error = "A name is required."
    elif not location:
        error = "A location is required"
    elif not start_time:
        error = "A start time is required"
    elif not end_time:
        error = "An end time is required"
    elif not description:
        error = "A description is required"

    if error is None:
        try:
            event = Event(name, location, start_time, end_time, description)
            db_session.add(event)
            db_session.commit()
        except exc.IntegrityError:
            db_session.rollback()
            error = f"An event with those details already exists!"
        else:
            return redirect(url_for("index"))

        flash(error)

    return render_template('auth/register.html')


