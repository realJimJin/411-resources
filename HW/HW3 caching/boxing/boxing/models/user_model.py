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
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    @staticmethod
    def _generate_hashed_password(password: str) -> tuple[str, str]:
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return salt, hashed_password

    @classmethod
    def create_user(cls, username: str, password: str) -> None:
        try:
            salt, hashed_password = cls._generate_hashed_password(password)
            user = cls(username=username, salt=salt, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            logger.info("User successfully added to the database: %s", username)
        except IntegrityError:
            logger.error("Duplicate username: %s", username)
            raise ValueError(f"Username {username} already exists.")
        except Exception as e:
            logger.error("Database error: %s", str(e))
            raise

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        user = cls.query.filter_by(username=username).first()
        if not user:
            raise ValueError(f"User {username} not found")
        
        salted_password = (user.salt + password).encode('utf-8')
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        
        return hashed_password == user.password

    @classmethod
    def delete_user(cls, username: str) -> None:
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")

        db.session.delete(user)
        db.session.commit()
        logger.info("User %s deleted successfully", username)

    def get_id(self) -> str:
        return str(self.id)

    @classmethod
    def get_id_by_username(cls, username: str) -> int:
        user = cls.query.filter_by(username=username).first()
        if not user:
            raise ValueError(f"User {username} not found")
        return user.id

    @classmethod
    def update_password(cls, username: str, new_password: str) -> None:
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        
        salt, hashed_password = cls._generate_hashed_password(new_password)
        user.salt = salt
        user.password = hashed_password

        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)