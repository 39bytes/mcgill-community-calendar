from flask import (Blueprint, render_template, request, redirect, url_for, abort)
from codejamapp import auth

from flask import (
    Blueprint, render_template, current_app
)
from codejamapp.database import db_session
from codejamapp.models import User

bp = Blueprint('user', __name__, url_prefix="/user")

@bp.route("/<int:id>/")
def user(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
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

