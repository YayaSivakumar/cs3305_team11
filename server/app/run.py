from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_from_directory, abort, url_for, jsonify

from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import os
import uuid
from dotenv import load_dotenv
from models.file import File
from models.user import User
from flask_login import LoginManager
from db import db

load_dotenv()  # Load environment variables from .env file


UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')  # Get the path to the uploads folder from the environment variables

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER  # Update path as needed

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    return app  # Return the Flask app instance


def cleanup_expired_files(app):
    with app.app_context():
        now = datetime.utcnow()
        expired_files = File.query.filter(File.expires_at <= now).all()
        for file in expired_files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.unique_id)
            if os.path.exists(filepath):
                os.remove(filepath)
            db.session.delete(file)
        db.session.commit()


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: cleanup_expired_files(app), trigger="interval", hours=1)
    scheduler.start()


if __name__ == '__main__':
    app_instance = create_app()
    import routes
    start_scheduler(app_instance)
