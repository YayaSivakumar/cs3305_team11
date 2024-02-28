from ..db import db

from .file import File

UploadedFiles = db.Table('uploaded_files',
                        db.Column('file_id', db.Integer, db.ForeignKey('file.id'), primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                        )
