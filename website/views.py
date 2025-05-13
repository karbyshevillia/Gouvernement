"""
This file contains the front-end views that determine the web interface.
"""

from flask import Blueprint

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    """
    Returns the home page of the website
    """
    return "<h1>Test</h1>"