"""
This file contains authentication management.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Returns the login page
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("There are no accounts registered under this email.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    """
    Returns the logout page
    """
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """
    Returns the sign up page
    """
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password_1 = request.form.get("password_1")
        password_2 = request.form.get("password_2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("An account with this email already exists.", category="error")
        elif len(email) < 4:
            flash("The email must be longer than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("The first name must be longer than 1 character.", category="error")
        elif password_1 != password_2:
            flash("Passwords do not match.", category="error")
        elif len(password_1) < 7:
            flash("The password must be longer than 6 characters.", category="error")
        else:
            new_user = User(email=email,
                            first_name=first_name,
                            password=generate_password_hash(password_1, method="scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)