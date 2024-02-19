from flask_sqlalchemy import SQLAlchemy
from server.app.run import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    email = db.Column(db.String(44), unique=True)
    password_hashed = db.Column(db.String(128))




