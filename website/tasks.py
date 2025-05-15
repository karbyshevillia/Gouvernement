"""
This file contains the front-end views that determine the web interface for tasks.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Project, Task
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .aux.tools import collaborators_input_is_valid
from datetime import datetime

tasks = Blueprint("tasks", __name__)


@tasks.route("/<parent_project_id>/initiate", methods=["GET", "POST"])
@login_required
def task_initiate(parent_project_id):
    """
    Returns the web page where a new task is created
    """
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        assignees = request.form.get("assignees")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(assignees)
        deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        status = bool(status)
        # print(clb, val)
        # print(deadline)

        if len(title) > 200:
            flash("The task title is too long (>200 characters).", category="error")
        elif len(description) > 1200:
            flash("The task description is too long (>1200 characters).", category="error")
        elif not val:
            flash("The assignees field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        else:
            parent_project = Project.query.get(parent_project_id)
            task = Task(title=title,
                        parent_project=parent_project.id,
                        priority=priority,
                        description=description,
                        assigned_by=current_user.id,
                        deadline=deadline,
                        current_assignees=[],
                        status=status)
            task.current_assignees.extend(clb)
            db.session.add(task)
            db.session.commit()
            flash("Task initiated successfully!", category="success")
            return redirect(f"/views/projects/{parent_project_id}")

    return render_template("tasks_init.html",
                           user=current_user,
                           parent_project_id=parent_project_id)


@tasks.route("/<parent_project_id>/task<task_id>")
@login_required
def task_info(parent_project_id, task_id):
    """
    Shews information about a Task as accessed
    through a Project Info page by clicking on a Task
    """
    task = Task.query.get(task_id)
    assigned_by = User.query.get(task.assigned_by).email
    assignee_emails = [user.email for user in task.current_assignees]

    return render_template("tasks_info.html",
                           user=current_user,
                           task=task,
                           assigned_by=assigned_by,
                           assignee_emails=assignee_emails,
                           parent_project_id=parent_project_id)


@tasks.route("/<parent_project_id>/task<task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task_info(parent_project_id, task_id):
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        assignees = request.form.get("assignees")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(assignees)
        deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
        status = bool(int(status))
        # print(clb, val)
        # print(deadline)

        if len(title) > 200:
            flash("The task title is too long (>200 characters).", category="error")
        elif len(description) > 1200:
            flash("The task description is too long (>1200 characters).", category="error")
        elif not val:
            flash("The assignees field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        else:
            task = Task.query.get(task_id)
            task.title = title
            task.priority = priority
            task.description = description
            task.deadline = deadline
            task.current_assignees = clb
            task.status = status
            db.session.commit()
            flash("Task info updated successfully!", category="success")
            return redirect(f"/tasks/{parent_project_id}/task{task_id}")

    task = Task.query.get(task_id)
    assignees_string = ", ".join([user.email for user in task.current_assignees])
    return render_template("tasks_edit.html",
                           user=current_user,
                           task=task,
                           assignees_string=assignees_string,
                           parent_project_id=parent_project_id)


@tasks.route("/<parent_project_id>/task<task_id>/delete", methods=["POST"])
@login_required
def delete_task(parent_project_id, task_id):
    task = Task.query.get(task_id)
    was = task.title
    was_project = Project.query.get(parent_project_id).title
    task.current_assignees.clear()
    db.session.delete(task)
    db.session.commit()
    flash(f"Task {was} has been deleted from project {was_project}.", "success")
    return redirect(f"/views/projects/{parent_project_id}")