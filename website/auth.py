"""
This file contains authentication management.
"""

from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
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

@auth.route("/sign-up")
def sign_up():
    """
    Returns the sign up page
    """
    return render_template("sign_up.html")