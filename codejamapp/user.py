import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from codejamapp.models import User

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc
from codejamapp.database import db_session

bp = Blueprint('user', __name__, url_prefix="/user")

@bp.route("/<int:id>/")
def user(id):
    user = User.query.get(id)
    return render_template('user/', user=user)

