from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(config_name=None):
    """Build and return the Flask application (the 'application factory')."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app