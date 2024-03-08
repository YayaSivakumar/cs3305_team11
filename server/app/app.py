import os
from datetime import datetime, timedelta
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from .db import db
from .login_manager import login_manager

from .models.file_upload import File
from .models.user import User

from .routes import register_routes

from .config import UPLOADS_FOLDER
from .config import SECRET_KEY


def create_app():
    """
    Create a Flask app and return it
    """
    app = Flask(__name__)
    # Set the app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
    app.config['SECRET_KEY'] = SECRET_KEY
    # Initialize the app with the database
    db.init_app(app)
    with app.app_context():
        # Create the database tables
        db.create_all()
    # Initialize the flask login manager
    login_manager.init_app(app)
    login_manager.login_view = 'user_routes.login'

    @login_manager.user_loader  # Add user_loader callback here
    def load_user(user_id):
        # This callback is used to reload the user object from the user ID stored in the session
        return User.query.get(int(user_id))

    # Register the all the routes' blueprints
    register_routes(app)  # Register routes here

    return app


def cleanup_expired_files(app):
    """
    Remove expired files from the database and the file system
    """
    with app.app_context():
        # Remove expired files from the database and the file system
        now = datetime.utcnow()
        # Get all the expired files
        expired_files = File.query.filter(File.expires_at <= now).all()
        for file in expired_files:
            # Remove the file from the file system
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.unique_id)
            if os.path.exists(filepath):
                os.remove(filepath)
            db.session.delete(file)
        db.session.commit()


def start_scheduler(app):
    """
    Start the scheduler to cleanup expired files
    """
    scheduler = BackgroundScheduler()
    # Schedule the cleanup_expired_files function to run every hour
    scheduler.add_job(func=lambda: cleanup_expired_files(app), trigger="interval", hours=1)
    scheduler.start()
