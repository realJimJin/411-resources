import hashlib
import logging
import os

from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError

from boxing.db import db
from boxing.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
=======
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)  # 16-byte salt in hex
    password = db.Column(db.String(64), nullable=False)  # SHA-256 hash in hex
>>>>>>> upstream/solutions

    @staticmethod
    def _generate_hashed_password(password: str) -> tuple[str, str]:
        """
        Generate a random salt and SHA-256 hash of salt+password.
        """
        salt = os.urandom(16).hex()
<<<<<<< HEAD
        hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return salt, hashed
=======
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password
>>>>>>> upstream/solutions

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        """
        Create a new user with a salted, hashed password.
        Raises ValueError if username already exists.
        """
<<<<<<< HEAD
        salt, hashed = cls._generate_hashed_password(password)
        user = cls(username=username, salt=salt, password=hashed)
        try:
            db.session.add(user)
            db.session.commit()
            logger.info("User created successfully: %s", username)
=======
        salt, hashed_password = cls._generate_hashed_password(password)
        new_user = cls(username=username, salt=salt, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info("User successfully added to the database: %s", username)
>>>>>>> upstream/solutions
        except IntegrityError:
            db.session.rollback()
            logger.error("Duplicate username: %s", username)
            raise ValueError(f"User with username '{username}' already exists")
<<<<<<< HEAD
=======
        except Exception as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            raise
>>>>>>> upstream/solutions

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        """
        Verify a user's password. Raises ValueError if user not found.
        Returns True if correct, False otherwise.
        """
        user = cls.query.filter_by(username=username).first()
<<<<<<< HEAD
        if user is None:
            raise ValueError(f"User {username} not found")
        hashed = hashlib.sha256((user.salt + password).encode('utf-8')).hexdigest()
        return hashed == user.password
=======
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        return hashed_password == user.password
>>>>>>> upstream/solutions

    @classmethod
    def delete_user(cls, username: str) -> None:
        """
        Delete a user by username. Raises ValueError if user not found.
        """
        user = cls.query.filter_by(username=username).first()
<<<<<<< HEAD
        if user is None:
            logger.error("User %s not found", username)
=======
        if not user:
            logger.info("User %s not found", username)
>>>>>>> upstream/solutions
            raise ValueError(f"User {username} not found")
        db.session.delete(user)
        db.session.commit()
        logger.info("User %s deleted successfully", username)

    def get_id(self) -> str:
        """
<<<<<<< HEAD
        Return this user's ID as a string (for Flask-Login).
        """
        return str(self.id)
=======
        Get the ID of the user.

        Returns:
            int: The ID of the user.
        """
        return self.username
>>>>>>> upstream/solutions

    @classmethod
    def get_id_by_username(cls, username: str) -> int:
        """
        Retrieve a user's numeric ID by username. Raises ValueError if not found.
        """
        user = cls.query.filter_by(username=username).first()
<<<<<<< HEAD
        if user is None:
=======
        if not user:
            logger.info("User %s not found", username)
>>>>>>> upstream/solutions
            raise ValueError(f"User {username} not found")
        return user.id

    @classmethod
    def update_password(cls, username: str, new_password: str) -> None:
        """
        Update an existing user's password. Raises ValueError if user not found.
        """
        user = cls.query.filter_by(username=username).first()
<<<<<<< HEAD
        if user is None:
            logger.error("User %s not found", username)
            raise ValueError(f"User {username} not found")
        salt, hashed = cls._generate_hashed_password(new_password)
        user.salt = salt
        user.password = hashed
        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)
=======
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")

        salt, hashed_password = cls._generate_hashed_password(new_password)
        user.salt = salt
        user.password = hashed_password
        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)
>>>>>>> upstream/solutions
