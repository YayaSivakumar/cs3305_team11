# from .files_uploaded import UploadedFiles
from ..db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bcrypt import hashpw, gensalt, checkpw


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_name = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship('File', backref='upload', lazy=True)
    download_count = db.Column(db.Integer, default=0)
    message = db.Column(db.String(500))
    hashed_password = db.Column(db.String(128), default=None)

    def __repr__(self):
        return f"<Upload {self.id}>"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # self.password_hashed = generate_password_hash(password)
        self.hashed_password = hashpw(password.encode('utf-8'), gensalt())

    def verify_password(self, password):
        # return check_password_hash(self.password_hashed, password)
        return checkpw(password.encode('utf-8'), self.hashed_password)

    def is_password_protected(self):
        return self.hashed_password is not None


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))




