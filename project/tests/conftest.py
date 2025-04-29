import pytest
from app import create_app, db

from app.models.favorite_location import FavoriteLocationModel
from app import create_app
from config import TestConfig

@pytest.fixture
def fav_model():
    return FavoriteLocationModel()

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session