import pytest
from app.models.user import User
@pytest.fixture
def sample_user_data():
    """Fixture providing sample user input data."""
    return {
        "username": "testuser",
        "password": "securepassword123"
    }

@pytest.fixture
def db_session(session):
    """Fixture to roll back session after each test for clean database."""
    yield session
    session.rollback()


# Create User

def test_create_user(db_session, sample_user_data):
    """Test creating a new user."""
    user = User(username=sample_user_data["username"])
    user.set_password(sample_user_data["password"])
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert fetched_user is not None, "User should exist in database after creation."
    assert fetched_user.username == sample_user_data["username"]
    assert len(fetched_user.salt) == 32, "Salt should be 32 characters (hex)."
    assert fetched_user.password_hash is not None

def test_create_duplicate_user(db_session, sample_user_data):
    """Test creating a duplicate user (should fail)."""
    user1 = User(username=sample_user_data["username"])
    user1.set_password(sample_user_data["password"])
    db_session.add(user1)
    db_session.commit()

    user2 = User(username=sample_user_data["username"])
    user2.set_password(sample_user_data["password"])
    db_session.add(user2)

    with pytest.raises(Exception):
        db_session.commit()  


# Password Checking

def test_check_correct_password(db_session, sample_user_data):
    """Test checking correct password."""
    user = User(username=sample_user_data["username"])
    user.set_password(sample_user_data["password"])
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert fetched_user.check_password(sample_user_data["password"]) is True

def test_check_incorrect_password(db_session, sample_user_data):
    """Test checking incorrect password."""
    user = User(username=sample_user_data["username"])
    user.set_password(sample_user_data["password"])
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert fetched_user.check_password("wrongpassword") is False


# Update Password

def test_update_password(db_session, sample_user_data):
    """Test updating user's password and verifying it."""
    user = User(username=sample_user_data["username"])
    user.set_password(sample_user_data["password"])
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    new_password = "newpassword456"
    fetched_user.set_password(new_password)
    db_session.commit()

    updated_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert updated_user.check_password(new_password) is True
    assert updated_user.check_password(sample_user_data["password"]) is False  # Old password should fail


# Delete User

def test_delete_user(db_session, sample_user_data):
    """Test deleting a user."""
    user = User(username=sample_user_data["username"])
    user.set_password(sample_user_data["password"])
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    db_session.delete(fetched_user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert deleted_user is None