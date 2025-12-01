import secrets
from flask import Flask
from .routes import main_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(32)
    app.register_blueprint(main_bp)
    return app
