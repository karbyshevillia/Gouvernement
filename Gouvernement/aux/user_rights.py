"""
Tools related to grant different kinds of users definite rights,
such as for project supervisors and collaborators,
for task assigners and assignees.
"""

from Gouvernement.models import User, Project, Task
from functools import wraps
import re
import datetime
from flask import redirect, url_for, request, flash
from flask_login import current_user
from inspect import signature


def role_required(check: callable, message: str, back_route_unauth: str):
    """
    A decorator that:
      1. Always passes `current_user` as the first argument to your `check`.
      2. Introspects `check`’s signature to pick up only the route kwargs it declares.
      3. If the check fails, flashes `message` and redirects to `referrer` or `back_route_unauth`.
    """
    sig = signature(check)
    param_names = list(sig.parameters.keys())[1:]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            check_args = [current_user]
            for name in param_names:
                if name in kwargs:
                    check_args.append(kwargs[name])
                else:
                    flash("Permission check mis-configured.", "error")
                    return redirect(request.referrer or back_route_unauth)

            allowed = check(*check_args)
            if not allowed:
                flash(message, "error")
                return redirect(request.referrer or back_route_unauth)

            return f(*args, **kwargs)
        return wrapper
    return decorator

def is_project_supervisor(user, project_id):
    project = Project.query.get(project_id)
    return project.supervisor == user.id

def is_project_collaborator(user, project_id):
    project = Project.query.get(project_id)
    return any(c.id == user.id for c in project.current_collaborators)

def is_project_supervisor_or_collaborator(user, project_id):
    return is_project_supervisor(user, project_id) or is_project_collaborator(user, project_id)

def is_task_assigner(user, task_id):
    task = Task.query.get(task_id)
    return task.assigned_by == user.id

def is_task_assignee(user, task_id):
    task = Task.query.get(task_id)
    return any(c.id == user.id for c in task.current_assignees)

def is_task_assigner_or_assignee(user, task_id):
    return is_task_assigner(user, task_id) or is_task_assignee(user, task_id)