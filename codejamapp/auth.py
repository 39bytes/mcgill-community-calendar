import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

import os 

from codejamapp.models import User
from codejamapp.utils import allowed_file, append_timestamp_and_hash

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc
from codejamapp.database import db_session

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form['email']
        password = request.form['password']
        image = request.files['userImage']
        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        
        
        if error is None:
            try:
                filename = ''
                if image and allowed_file(image.filename):
                    filename = append_timestamp_and_hash(image.filename)
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                u = User(name, email, generate_password_hash(password), filename)
                db_session.add(u)
                db_session.commit()
            except exc.IntegrityError:
                db_session.rollback()
                if filename:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                error = f"User with that email already exists!"
            else:
                return redirect(url_for("auth.login"))
        
        # Send error message to template
        flash(error)

    # If there was a GET request or an error while registering,
    # just render the plain form
    return render_template('auth/register.html')

@bp.route('/login', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        # Input validation
        if not email:
            error = "Name is required."
        elif not password:
            error = "Password is required."

        # Username and password are not empty
        if error is None:
            user = User.query.filter(User.email == email).first()
            
            if user is None or not check_password_hash(user.password, password):
                error = "Incorrect credentials"

        # User logged in successfully
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view