"""
This file contains the front-end views that determine the web interface for tasks.
"""

from flask import (Blueprint,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for)
from .models import (User,
                     Project,
                     Task)
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from . import db
from flask_login import (login_user,
                         login_required,
                         logout_user,
                         current_user)
from .aux.tools import (collaborators_input_is_valid,
                        task_search)
from .aux.user_rights import (role_required,
                              is_task_assigner,
                              is_task_assignee,
                              is_task_assigner_or_assignee,
                              is_project_collaborator,
                              is_project_supervisor_or_collaborator)
from .aux.task_rights import (attr_required,
                              project_is_open)
from datetime import datetime
from sqlalchemy import or_, and_

tasks = Blueprint("tasks", __name__)

@tasks.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks_view():
    """
    Returns the Tasks page of the Gouvernement
    """
    tasks_list = Task.query.filter(or_(Task.assigned_by == current_user.id,
                                       Task.current_assignees.contains(current_user)))
    if request.method == "POST":
        search_string = request.form.get("filters")
        tasks_list = task_search(search_string, tasks_list)
    if request.method == "GET":
        tasks_list = task_search("status=<OPEN>, priority_sort=<DESC>", tasks_list)

    parent_projects_list = [Project.query.get(task.parent_project) for task in tasks_list]
    zipped = list(zip(tasks_list, parent_projects_list))
    tasks_assigners = dict(zip(zipped, [User.query.get(task.assigned_by) for task in tasks_list]))
    return render_template("tasks/tasks.html",
                           user=current_user,
                           tasks_assigners=tasks_assigners)


@tasks.route("/project/<int:project_id>/initiate", methods=["GET", "POST"])
@login_required
@role_required(is_project_collaborator,
               "You have to be a current collaborator to this project to be able to initiate a task.",
               "/views/projects")
@attr_required(project_is_open,
               "The project supervisor has closed this project. Tasks can no longer be initiated or edited.",
               "/views/projects/<int:project_id>")
def task_initiate(project_id):
    """
    Governs the web page where a new task is created
    """
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        assignees = request.form.get("assignees")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(assignees)

        if not 1 <= len(title) <= 200:
            flash("The task title length must be between 1 and 200 characters.", category="error")
        elif not priority:
            flash("The task priority within the project has not been set.", category="error")
        elif not 1 <= len(description) <= 1200:
            flash("The task description length must be between 1 and 1200 characters.", category="error")
        elif not deadline:
            flash("The task deadline has not been set.", category="error")
        elif not val:
            flash("The assignees field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        elif not status:
            flash("The task status has not been set.", category="error")
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            status = bool(int(status))
            parent_project = Project.query.get(project_id)
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
            return redirect(f"/views/projects/{project_id}")

    return render_template("tasks/tasks_init.html",
                           user=current_user,
                           parent_project_id=project_id)


@tasks.route("/project/<int:project_id>/task/<int:task_id>")
@login_required
@role_required(is_task_assigner_or_assignee,
               "You have to have assigned this task or be an assignee to be able to view its info.",
               "/views/projects")
def task_info(project_id, task_id):
    """
    Shews information about a Task as accessed
    through a Project Info page by clicking on a Task
    """
    task = Task.query.get(task_id)
    assigned_by = User.query.get(task.assigned_by).email
    assignee_emails = [user.email for user in task.current_assignees]

    return render_template("tasks/tasks_info.html",
                           user=current_user,
                           task=task,
                           assigned_by=assigned_by,
                           assignee_emails=assignee_emails,
                           parent_project_id=project_id)


@tasks.route("/task/<int:task_id>")
@login_required
@role_required(is_task_assigner_or_assignee,
               "You have to have assigned this task or be an assignee to be able to view its info.",
               "/views/projects")
def task_disjoint_info(task_id):
    """
    Shews information about a Task as accessed
    through a Project Info page by clicking on a Task
    """
    task = Task.query.get(task_id)
    project_id = task.parent_project
    assigned_by = User.query.get(task.assigned_by).email
    assignee_emails = [user.email for user in task.current_assignees]

    return render_template("tasks/tasks_disjoint_info.html",
                           user=current_user,
                           task=task,
                           assigned_by=assigned_by,
                           assignee_emails=assignee_emails,
                           parent_project_id=project_id)

@tasks.route("/project/<int:project_id>/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
@role_required(is_task_assigner,
               "You have to have assigned this task to be able to edit its info.",
               "/views/projects")
@attr_required(project_is_open,
               "The project supervisor has closed this project. Tasks can no longer be initiated or edited.",
               "/views/projects/<int:project_id>")
def edit_task_info(project_id, task_id):
    """
    Governs the page for task editing
    """
    if request.method == "POST":
        title = request.form.get("title")
        priority = request.form.get("priority")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        assignees = request.form.get("assignees")
        status = request.form.get("status")

        clb, val = collaborators_input_is_valid(assignees)

        if not 1 <= len(title) <= 200:
            flash("The task title length must be between 1 and 200 characters.", category="error")
        elif not priority:
            flash("The task priority within the project has not been set.", category="error")
        elif not 1 <= len(description) <= 1200:
            flash("The task description length must be between 1 and 1200 characters.", category="error")
        elif not deadline:
            flash("The task deadline has not been set.", category="error")
        elif not val:
            flash("The assignees field is either improperly filled out, "
                  "or some email is unregistered.", category="error")
        elif not status:
            flash("The task status has not been set.", category="error")
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
            status = bool(int(status))
            task = Task.query.get(task_id)
            task.title = title
            task.priority = priority
            task.description = description
            task.deadline = deadline
            task.current_assignees = clb
            task.status = status
            db.session.commit()
            flash("Task info updated successfully!", category="success")
            return redirect(f"/tasks/project/{project_id}/task/{task_id}")

    task = Task.query.get(task_id)
    assignees_string = ", ".join([user.email for user in task.current_assignees])
    return render_template("tasks/tasks_edit.html",
                           user=current_user,
                           task=task,
                           assignees_string=assignees_string,
                           parent_project_id=project_id)


@tasks.route("/project/<int:project_id>/task/<int:task_id>/delete", methods=["POST"])
@login_required
@role_required(is_task_assigner,
               "You have to have assigned this task to be able to delete it.",
               "/views/projects")
def delete_task(project_id, task_id):
    """
    Governs the page for task deletion
    """
    task = Task.query.get(task_id)
    was = task.title
    was_project = Task.query.get(project_id).title
    task.current_assignees.clear()
    db.session.delete(task)
    db.session.commit()
    flash(f"Task {was} has been deleted from project {was_project}.", "success")
    return redirect(f"/views/projects/{project_id}")

@tasks.route("/task/<int:task_id>/parent=<int:project_id>", methods=["GET", "POST"])
@login_required
@role_required(is_project_supervisor_or_collaborator,
               "You have to supervise this project or be its current collaborator to be able to view its info.",
               "/tasks/tasks")
def project_from_task_info(task_id, project_id):
    """
    Shews information about a Project as accessed
    through the Tasks tab by clicking on 'See Project Info'
    in Task Info
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

    return render_template("projects/project_from_task_info.html",
                           user=current_user,
                           project=project,
                           supervisor=supervisor,
                           collaborator_emails=collaborator_emails,
                           tasks_assigned_by=tasks_assigned_by,
                           referrer_task_id=task_id)