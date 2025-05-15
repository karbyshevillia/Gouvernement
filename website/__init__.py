from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Initialisation of a Flask app running as a WSGI server
    """

    app = Flask(__name__, instance_path="/Users/illiaknu/Gouvernement")
    app.config["SECRET_KEY"] = "314159265358979323846264339"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .tasks import tasks

    app.register_blueprint(views, url_prefix="/views")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(tasks, url_prefix="/tasks")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app

def create_database(app):
    if not path.exists("/Users/illiaknu/Gouvernement" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database Created!")