from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Initialisation of a Flask app running as a WSGI server
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "314159265358979323846264339"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/views")
    app.register_blueprint(auth, url_prefix="/auth")

    return app