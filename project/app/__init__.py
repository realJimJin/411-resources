from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()


def create_app():
    """App factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    db.init_app(app)
    Session(app)

    # Register blueprints
    from .routes.account_management import account_mgmt_bp
    from .routes.favorite_locations import favorite_locations_bp
    app.register_blueprint(account_mgmt_bp)
    app.register_blueprint(favorite_locations_bp)

    # Healthcheck route
    @app.route('/healthcheck')
    def healthcheck():
        return {'status': 'ok'}, 200

    return app