"""
This file contains the front-end views that determine the web interface.
"""

from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    """
    Returns the home page of the website
    """
    return render_template("home.html")