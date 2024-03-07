from ..db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bcrypt import hashpw, gensalt, checkpw

# from .files_uploaded import UploadedFiles


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    email = db.Column(db.String(44), unique=True)
    hashed_password = db.Column(db.String(128))
    uploads = db.relationship('Upload', backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # self.password_hashed = generate_password_hash(password)
        self.hashed_password = hashpw(password.encode('utf-8'), gensalt())

    def verify_password(self, password):
        return checkpw(password.encode('utf-8'), self.hashed_password)




