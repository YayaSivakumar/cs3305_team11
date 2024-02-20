import os
from datetime import datetime, timedelta
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from .db import db
from .models.file import File
from .models.user import User
from .routes import main_routes as m, file_routes as f, user_routes as u
from flask_login import LoginManager
from .config import UPLOADS_FOLDER


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader  # Add user_loader callback here
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(m.main_routes)
    app.register_blueprint(f.file_routes)
    app.register_blueprint(u.user_routes)

    return app


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
