"""
This file contains the front-end views that determine the web interface.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Project, Task
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .aux.tools import collaborators_input_is_valid, project_search, task_search
from .aux.user_rights import (role_required,
                              is_project_supervisor,
                              is_project_collaborator,
                              is_project_supervisor_or_collaborator)
from datetime import datetime
from sqlalchemy import or_, and_

views = Blueprint("views", __name__)

@views.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    """
    Returns the home page of the Gouvernement
    """
    # projects_list = list(set(current_user.projects) | set(current_user.supervised_projects))
    projects_list = Project.query.filter(or_(Project.supervisor == current_user.id,
                                          Project.current_collaborators.contains(current_user)))
    if request.method == "POST":
        search_string = request.form.get("filters")
        projects_list = project_search(search_string, projects_list)

    projects_supervisors = dict(zip(projects_list, [User.query.get(project.supervisor) for project in projects_list]))
    return render_template("projects.html", user=current_user, projects_supervisors=projects_supervisors)

@views.route("/initiate", methods=["GET", "POST"])
@login_required
def project_initiate():
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

        if not 1 <= len(title) <= 200:
            flash("The project title length must be between 1 and 200 characters.", category="error")
        elif not priority:
            flash("The project priority has not been set.", category="error")
        elif not 1 <= len(description) <= 1200:
            flash("The project description length must be between 1 and 1200 characters.", category="error")
        elif not deadline:
            flash("The project deadline has not been set.", category="error")
        elif not val:
            flash("The collaborators field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        elif not status:
            flash("The project status has not been set.", category="error")
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            status = bool(int(status))
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

@views.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
@role_required(is_project_supervisor,
               "You have to supervise this project to be able to edit its info.",
               "/views/projects/<project_id>")
def edit_project_info(project_id):
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        collaborators = request.form.get("collaborators")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(collaborators)

        if not 1 <= len(title) <= 200:
            flash("The project title length must be between 1 and 200 characters.", category="error")
        elif not priority:
            flash("The project priority has not been set.", category="error")
        elif not 1 <= len(description) <= 1200:
            flash("The project description length must be between 1 and 1200 characters.", category="error")
        elif not deadline:
            flash("The project deadline has not been set.", category="error")
        elif not val:
            flash("The collaborators field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        elif not status:
            flash("The project status has not been set.", category="error")
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            status = bool(int(status))
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

@views.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
@role_required(is_project_supervisor,
               "You have to supervise this project to be able to delete it.",
               "/views/projects/<project_id>")
def delete_project(project_id):
    project = Project.query.get(project_id)
    was = project.title
    project.current_collaborators.clear()
    db.session.delete(project)
    db.session.commit()
    flash(f"Project {was} has been deleted.", "success")
    return redirect(url_for("views.projects"))

@views.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
@role_required(is_project_supervisor_or_collaborator,
               "You have to supervise this project or be its current collaborator to be able to view its info.",
               "/views/projects")
def projects_info(project_id):
    """
    Shews information about a Project as accessed
    through the Projects tab by clicking on a Project
    """
    project = Project.query.get(project_id)
    supervisor = User.query.get(project.supervisor).email
    collaborator_emails = [user.email for user in project.current_collaborators]

    tasks_list = Task.query.filter(and_(or_(Task.assigned_by == current_user.id,
                                       Task.current_assignees.contains(current_user)),
                                       Task.parent_project == project_id))
    if request.method == "POST":
        search_string = request.form.get("filters")
        tasks_list = task_search(search_string, tasks_list)

    tasks_assigned_by = dict(zip(tasks_list, [User.query.get(task.assigned_by) for task in tasks_list]))

    return render_template("projects_info.html",
                           user=current_user,
                           project=project,
                           supervisor=supervisor,
                           collaborator_emails=collaborator_emails,
                           tasks_assigned_by=tasks_assigned_by)