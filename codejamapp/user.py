from flask import (Blueprint, render_template, request, redirect, url_for, abort)
from codejamapp import auth

from flask import (
    Blueprint, render_template, current_app
)
from codejamapp.database import db_session
from codejamapp.models import User
from codejamapp.utils import append_timestamp_and_hash

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

        new_image = request.files["userImage"]
        new_filename = user.pfp_filename

        if new_image:
            if user.pfp_filename:
                filename = user.pfp_filename
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_filename = append_timestamp_and_hash(new_image.filename)
            new_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))

        setattr(user, "name", name)
        setattr(user, "description", description)
        setattr(user, "pfp_filename", new_filename)
        db_session.commit()

        return redirect(url_for("user.user", id=user.id))

    return render_template("user/edit.html", user=user)

