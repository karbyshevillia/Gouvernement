from flask import Flask

def create_app():
    """
    Initialisation of the Flask app
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "31415926535"

    return app