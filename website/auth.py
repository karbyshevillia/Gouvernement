"""
This file contains authentication management.
"""

from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    """
    Returns the login page
    """
    return "<p>Log In</p>"

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
    return "<p>Sign Up</p>"