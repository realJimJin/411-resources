from flask import Flask
from flask_session import Session
from .extensions import db
import os

def create_app(config_class=None):
    """App factory to create and configure the Flask app."""
    app = Flask(__name__)

    # If a config_class is passed (like TestConfig during testing), use it
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    Session(app)

    from .routes.account_management import account_mgmt_bp
    from .routes.favorite_locations import favorite_locations_bp
    app.register_blueprint(account_mgmt_bp)
    app.register_blueprint(favorite_locations_bp)

    @app.route('/healthcheck')
    def healthcheck():
        return {'status': 'ok'}, 200

    return app