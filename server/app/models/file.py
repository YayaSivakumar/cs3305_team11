from .files_uploaded import UploadedFiles
from ..db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    message = db.Column(db.String(500))
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=0)
    # user = db.relationship('User', secondary=UploadedFiles, backref='file', lazy='dynamic')
    # hashed_password = db.Column(db.String(128))

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

