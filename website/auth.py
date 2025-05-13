"""
This file contains authentication management.
"""

from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Returns the login page
    """
    return render_template("login.html")

@auth.route("/logout")
def logout():
    """
    Returns the logout page
    """
    return "<p>Log Out</p>"

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

        if len(email) < 4:
            flash("The email must be longer than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("The first name must be longer than 1 character.", category="error")
        elif password_1 != password_2:
            flash("Passwords do not match.", category="error")
        elif len(password_1) < 7:
            flash("The email must be longer than 6 characters.", category="error")
        else:
            flash("Account created!", category="success")
            pass

    return render_template("sign_up.html")