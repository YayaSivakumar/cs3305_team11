from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_from_directory, abort, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
import os
import uuid
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

db = SQLAlchemy()  # Create a SQLAlchemy database instance

UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')  # Get the path to the uploads folder from the environment variables


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    message = db.Column(db.String(500))
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    download_count = db.Column(db.Integer, default=0)
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


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER  # Update path as needed

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        '''This function handles file uploads. It accepts POST requests with a file, message, expiration_hours, and password fields.'''
        if request.method == 'POST':
            message = request.form.get('message', '')
            expiration_hours = int(request.form.get('expiration_hours', 24))
            password = request.form.get('password', '')
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename) # Sanitize the filename, prevent path traversal attacks
                unique_id = str(uuid.uuid4())
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
                file.save(filepath)
                expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
                new_file = File(filename=filename, unique_id=unique_id, message=message, expires_at=expires_at)
                new_file.password: str = password
                db.session.add(new_file)
                db.session.commit()
                link = url_for('download_file_page', unique_id=unique_id, _external=True)
                return jsonify({'message': 'File uploaded successfully.', 'link': link})

        else:
            # If it's not a POST request, just render the template without context
            return render_template('upload_success.html')

    @app.route('/uploaded/<unique_id>', methods=['GET'])
    def uploaded(unique_id):
        file = File.query.filter_by(unique_id=unique_id).first()
        if file:
            return render_template('uploaded.html', file=file)
        else:
            return "File not found", 404

    @app.route('/download/<unique_id>')
    def download_file_page(unique_id):
        print(unique_id)
        print(File.query.all())
        file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
        file_details = {
            'filename': file_record.filename,
            'message': file_record.message,
            'expires_at': file_record.expires_at,
            'download_link': url_for('direct_download_file', unique_id=unique_id, _external=True)
        }

        return render_template('download.html', file=file_details)

    @app.route('/download/file/<unique_id>')
    def direct_download_file(unique_id):
        # Fetch the file record using the unique ID from the database
        file_record = File.query.filter_by(unique_id=unique_id).first_or_404()

        # Check if the file has expired
        if datetime.utcnow() > file_record.expires_at:
            abort(410)  # 410 Gone indicates that the resource is no longer available and will not be available again.

        # Build the filepath using the UPLOAD_FOLDER setting and the unique file identifier
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)

        # Check if the file exists in the filesystem
        if not os.path.isfile(filepath):
            abort(404)  # 404 Not Found if the file does not exist on the server

        # Increment the download_count by 1
        file_record.download_count += 1
        db.session.commit()

        # Serve the file for download, using the original filename for the download
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                                   path=unique_id,
                                   as_attachment=True,
                                   download_name=file_record.filename)


    @app.route('/upload/success/<unique_id>')
    def upload_success(unique_id):
        file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
        file_details = {
            'url': url_for('download_file_page', unique_id=unique_id, _external=True),
            'filename': file_record.filename,
            'message': file_record.message,
            'expires_at': file_record.expires_at,
            'download_link': url_for('direct_download_file', unique_id=unique_id, _external=True),
            'download_count': file_record.download_count
        }
        return render_template('upload_success.html', file=file_details)

    return app # Return the Flask app instance


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
    start_scheduler(app_instance)
    app_instance.run(debug=True)
