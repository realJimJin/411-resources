from app import db
import os
import binascii
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """SQLAlchemy User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    def set_password(self, password):
        """Generates salt and hashes password."""
        self.salt = binascii.hexlify(os.urandom(16)).decode()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        """Checks the password against the stored hash and salt."""
        return check_password_hash(self.password_hash, password + self.salt)