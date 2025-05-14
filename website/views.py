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

@views.route("/initiate", methods=["GET", "POST"])
@login_required
def initiate():
    """
    Returns the web page where a new project is created
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

    return render_template("projects_init.html", user=current_user)

@views.route("/projects/<project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project_info(project_id):
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
            project = Project.query.get(project_id)
            project.title = title
            project.priority = priority
            project.description = description
            project.deadline = deadline
            project.current_collaborators = clb
            project.status = status
            db.session.commit()
            flash("Project info updated successfully!", category="success")
            return redirect(f"/views/projects/{project_id}")

    project = Project.query.get(project_id)
    collaborators_string = ", ".join([user.email for user in project.current_collaborators])
    return render_template("projects_edit.html",
                           user=current_user,
                           project=project,
                           collaborators_string=collaborators_string)

@views.route("/projects/<project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    was = project.title
    project.current_collaborators.clear()
    db.session.delete(project)
    db.session.commit()
    flash(f"Project {was} has been deleted.", "success")
    return redirect(url_for("views.projects"))

@views.route("/projects/<project_id>")
@login_required
def projects_info(project_id):
    """
    Shews information about a Project as accessed
    through the Projects tab by clicking on a Project
    """
    project = Project.query.get(project_id)
    supervisor = User.query.get(project.supervisor).email
    collaborator_emails = [user.email for user in project.current_collaborators]
    return render_template("projects_info.html",
                           user=current_user,
                           project=project,
                           supervisor=supervisor,
                           collaborator_emails=collaborator_emails)