"""
Functions that generate a random database
for project overviews
"""

from datetime import datetime, timedelta
from faker import Faker
from Gouvernement import db
from main import app
from Gouvernement.models import User, Project, Task
from werkzeug.security import generate_password_hash
import random

fake = Faker()

def create_sample_data():
    """
    Populates a random database using the Faker module
    """
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create Users
        users = []
        for _ in range(10):
            user = User(
                email=fake.unique.email(),
                password=generate_password_hash("password", method="scrypt"),
                first_name=fake.first_name()
            )
            db.session.add(user)
            users.append(user)

        db.session.commit()

        # Create Projects
        projects = []
        for _ in range(15):
            supervisor = random.choice(users)
            collaborators = random.sample(users, k=random.randint(2, 5))
            project = Project(
                title=fake.catch_phrase(),
                priority=random.randint(1, 5),
                description=fake.paragraph(nb_sentences=5),
                supervisor=supervisor.id,
                supervisor_user=supervisor,
                deadline=datetime.now() + timedelta(days=random.randint(10, 90)),
                status=random.choice([True, False])
            )
            project.current_collaborators = collaborators
            db.session.add(project)
            projects.append(project)

        db.session.commit()

        # Create Tasks
        for _ in range(150):
            parent_project = random.choice(projects)
            assigner = random.choice(users)
            assignees = random.sample(users, k=random.randint(1, 6))
            task = Task(
                parent_project=parent_project.id,
                title=fake.bs().capitalize(),
                priority=random.randint(1, 5),
                description=fake.text(max_nb_chars=300),
                assigned_by=assigner.id,
                assigned_by_user=assigner,
                deadline=datetime.now() + timedelta(days=random.randint(5, 45)),
                status=random.choice([True, False])
            )
            task.current_assignees = assignees
            db.session.add(task)

        db.session.commit()

        print("🌱 Sample data populated with Faker.")

if __name__ == "__main__":
    create_sample_data()
