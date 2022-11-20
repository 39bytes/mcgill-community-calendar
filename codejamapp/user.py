from flask import (Blueprint, render_template, request, redirect, url_for)
from codejamapp import auth
import os

from flask import (
    Blueprint, render_template, current_app
)
from codejamapp.models import User

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc
from codejamapp.database import db_session
from codejamapp.models import User

bp = Blueprint('user', __name__, url_prefix="/user")

@bp.route("/<int:id>/")
def user(id):
    user = User.query.get(id)
    return render_template('user/user.html', user=user)

@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@auth.login_required
def edit(id):
    user = User.query.get(id)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        setattr(user, "name", name)
        setattr(user, "description", description)
        db_session.commit()

        return redirect(url_for("user.user", id=user.id))
    return render_template("user/edit.html", user=user)

