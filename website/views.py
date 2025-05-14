"""
This file contains the front-end views that determine the web interface.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Project
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .aux.tools import collaborators_input_is_valid
from datetime import datetime

views = Blueprint("views", __name__)

@views.route("/projects")
@login_required
def projects():
    """
    Returns the home page of the website
    """
    projects_list = list(set(current_user.projects) | set(current_user.supervised_projects))
    projects_supervisors = dict(zip(projects_list, [User.query.get(project.supervisor) for project in projects_list]))
    return render_template("projects.html", user=current_user, projects_supervisors=projects_supervisors)

@views.route("/editing", methods=["GET", "POST"])
@login_required
def editing():
    """
    Returns the web page where a new project is created
    or an old one is modified
    """
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        collaborators = request.form.get("collaborators")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(collaborators)
        deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        status = bool(status)
        # print(clb, val)
        # print(deadline)

        if len(title) > 200:
            flash("The project title is too long (>200 characters).", category="error")
        elif len(description) > 1200:
            flash("The project description is too long (>1200 characters).", category="error")
        elif not val:
            flash("The collaborators field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        else:
            project = Project(title=title,
                              priority=priority,
                              description=description,
                              supervisor=current_user.id,
                              deadline=deadline,
                              current_collaborators=[],
                              status=status)
            project.current_collaborators.extend(clb)
            # print(project.current_collaborators)
            db.session.add(project)
            db.session.commit()
            flash("Project initiated successfully!", category="success")
            return redirect(url_for("views.projects"))

    return render_template("projects_edit.html", user=current_user)