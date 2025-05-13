"""
This file contains code related to the contents of the main database.
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

user_project = db.Table("user_project",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("project_id", db.Integer, db.ForeignKey("project.id")))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    priority = db.Column(db.Integer)
    description = db.Column(db.String(1200))
    supervisor = db.Column(db.Integer, db.ForeignKey("user.id"))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    deadline = db.Column(db.DateTime)
    current_collaborators = db.relationship("User", secondary=user_project, backref="on_projects")
    # tasks
    status = db.Column(db.Boolean)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship("Project", secondary=user_project, backref="collaborators")
    # notes = db.relationship("Note") # like a list of note id-s