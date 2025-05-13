"""
This file contains the front-end views that determine the web interface.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/home")
@login_required
def home():
    """
    Returns the home page of the website
    """
    return render_template("home.html", user=current_user)