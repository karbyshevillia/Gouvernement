"""
This file contains code related to the contents of the main database.
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func, case, select
from sqlalchemy.ext.hybrid import hybrid_property


user_project = db.Table("user_project",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("project_id", db.Integer, db.ForeignKey("project.id")))

user_task = db.Table("user_task",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("task_id", db.Integer, db.ForeignKey("task.id")))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    priority = db.Column(db.Integer)
    description = db.Column(db.String(1200))
    supervisor = db.Column(db.Integer, db.ForeignKey("user.id"))
    supervisor_user = db.relationship("User", back_populates="supervised_projects")
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline = db.Column(db.DateTime)
    current_collaborators = db.relationship("User", secondary=user_project, back_populates="projects")
    status = db.Column(db.Boolean)


    @hybrid_property
    def progress(self):
        lst = Task.query.filter_by(parent_project=self.id).all()
        bool_list = [task.status for task in lst]
        if len(bool_list) == 0:
            return 100
        in_calc = [e for e in bool_list if not e]
        return int(len(in_calc) / len(bool_list) * 100)

    @progress.expression
    def progress(cls):
        total = func.count(Task.id)
        completed = func.sum(case((Task.status == True, 1), else_=0))
        pct_expr = case(
            (total == 0, 100),
            else_=completed * 100.0 / total
        )
        return (
            select(pct_expr)
            .where(Task.parent_project == cls.id)
            .scalar_subquery()
        )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship("Project",
                               secondary=user_project,
                               back_populates="current_collaborators")
    tasks = db.relationship("Task",
                               secondary=user_task,
                               back_populates="current_assignees")
    supervised_projects = db.relationship("Project", back_populates="supervisor_user")
    assigned_tasks = db.relationship("Task", back_populates="assigned_by_user")
    has_assigned_tasks = db.relationship("Task")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_project = db.Column(db.Integer, db.ForeignKey("project.id"))
    title = db.Column(db.String(200))
    priority = db.Column(db.Integer)
    description = db.Column(db.String(1200))
    assigned_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    assigned_by_user = db.relationship("User", back_populates="assigned_tasks")
    assignment_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline = db.Column(db.DateTime)
    current_assignees = db.relationship("User", secondary=user_task, back_populates="tasks")
    status = db.Column(db.Boolean)