
from app import db
import os
import binascii
from werkzeug.security import generate_password_hash, check_password_hash

import logging
from app.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

class User(db.Model):
    """SQLAlchemy User model for authentication.
    
        id (int): Unique ID for all users
        username (str): Unique user for each user
        password_hash (str): password of user 
        salt (str)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    def set_password(self, password):
        """Generates salt and hashes password.
        
        Args: 
            password (str): Password for user
        
        """

        logger.info(f"Setting password {password}")
        self.salt = binascii.hexlify(os.urandom(16)).decode()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        """Checks the password against the stored hash and salt.
        
            Args: 
                password (str): Password inputted for user
        """
        logger.info(f"Setting password {password}")

        return check_password_hash(self.password_hash, password + self.salt)