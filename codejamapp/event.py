from flask import (Blueprint, request, url_for, redirect, render_template, flash, g, abort)
from codejamapp.models import Event, User
from codejamapp import auth
from codejamapp.database import db_session
from sqlalchemy import exc

bp = Blueprint('event', __name__, url_prefix="/event")

@bp.route("/<int:id>/info", methods=("GET",))
def info(id):
    event = Event.query.filter(Event.id == id).first()
    if event is None:
        abort(404)
    return render_template("event/info.html", event=event)


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@auth.login_required
def edit():
    event = Event.query.filter(Event.id == id).first()
    if request.method == "POST":
        # update event
        return redirect(url_for("event.info"))
    return redirect(url_for("index"))

@bp.route("/create", methods=("GET", "POST"))
@auth.login_required
def create():
    if request.method == "POST":
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
                event = Event(name, g.user.id, description, location, start_time, end_time)
                db_session.add(event)
                db_session.commit()
            except exc.IntegrityError:
                db_session.rollback()
                error = f"An event with those details already exists!"
            else:
                return redirect(url_for("event.info", id=event.id))

            flash(error)

    return render_template('event/create.html')


