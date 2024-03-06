# from .files_uploaded import UploadedFiles
from ..db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_name = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship('File', backref='upload', lazy=True)
    download_count = db.Column(db.Integer, default=0)
    message = db.Column(db.String(500))

    def __repr__(self):
        return f"<Upload {self.id}>"


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    hashed_password = db.Column(db.String(128))

    @property
    def password(self):  # This is a getter method for the password property
        '''The password property is a read-only property.
        It raises an AttributeError when accessed. This is because the password should not be read directly from the database.
        Instead, the verify_password method should be used to compare a password with the hashed password stored in the database.'''
        raise AttributeError('password is not a readable attribute')

    @password.setter  # This is a setter method for the password property
    def password(self, password):
        '''The password setter method is used to hash the password before storing it in the database.'''
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):  # This is a method to verify the password
        ''' The verify_password method is used to compare a password with the hashed password stored in the database.'''
        return check_password_hash(self.hashed_password, password)

