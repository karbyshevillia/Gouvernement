"""
Tools that define the rights of users depending
more generally on the database objects
"""

from Gouvernement.models import User, Project, Task
from functools import wraps
import re
import datetime
from flask import redirect, url_for, request, flash
from flask_login import current_user
from inspect import signature


def attr_required(check: callable, message: str, back_route_false: str):
    """
    A decorator that:
      1. Introspects the signature of the `check` function to pick up only the route kwargs it declares.
      2. If the check fails, flashes `message` and redirects to `referrer` or `back_route_false`.
    """
    sig = signature(check)
    param_names = list(sig.parameters.keys())

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            check_args = []
            for name in param_names:
                if name in kwargs:
                    check_args.append(kwargs[name])
                else:
                    flash("Permission check mis-configured.", "error")
                    return redirect(request.referrer or back_route_false)

            allowed = check(*check_args)
            if not allowed:
                flash(message, "error")
                return redirect(request.referrer or back_route_false)

            return f(*args, **kwargs)
        return wrapper
    return decorator


def project_is_open(project_id: Project):
    """
    Checks if a given project is OPEN by status
    """
    project = Project.query.get(project_id)
    return project.status