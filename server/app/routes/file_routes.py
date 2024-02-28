import os
import uuid
from datetime import datetime, timedelta
from flask import Blueprint
from flask import request, render_template, send_from_directory, abort, url_for, jsonify
from werkzeug.utils import secure_filename
from ..db import db
from ..config import UPLOADS_FOLDER

from ..models.file import File

from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

file_routes = Blueprint('file_routes', __name__)


@file_routes.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    This function handles file uploads. It accepts POST requests with a file, message, expiration_hours,
    and password fields.
    """
    if request.method == 'POST':
        message = request.form.get('message', '')
        expiration_hours = int(request.form.get('expiration_hours', 24))
        # password = request.form.get('password', '')
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)  # Sanitize the filename, prevent path traversal attacks
            unique_id = str(uuid.uuid4())
            filepath = os.path.join(UPLOADS_FOLDER, unique_id)
            file.save(filepath)
            expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
            new_file = File(filename=filename, unique_id=unique_id, message=message, expires_at=expires_at)

            # new_file.password: str = password
            db.session.add(new_file)
            db.session.commit()
            link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
            print(link)
            return jsonify({'message': 'File uploaded successfully.', 'link': link})

    else:
        # If it's not a POST request, just render the template without context
        return render_template('upload.html',
                               user_routes=user_routes,
                               file_routes=file_routes,
                               main_routes=main_routes)


@file_routes.route('/uploaded/<unique_id>', methods=['GET'])
def uploaded(unique_id):
    file = File.query.filter_by(unique_id=unique_id).first()
    if file:
        return render_template('uploaded.html',
                               file=file,
                               user_routes=user_routes,
                               file_routes=file_routes,
                               main_routes=main_routes)
    else:
        return "File not found", 404


@file_routes.route('/download/<unique_id>')
def download_file_page(unique_id):
    print(unique_id)
    print(File.query.all())
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    file_details = {
        'filename': file_record.filename,
        'message': file_record.message,
        'expires_at': file_record.expires_at,
        'download_link': url_for('file_routes.direct_download_file',
                                 unique_id=unique_id,
                                 _external=True)
    }

    return render_template('download.html',
                           file=file_details,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/download/file/<unique_id>')
def direct_download_file(unique_id):
    # Fetch the file record using the unique ID from the database
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()

    # Check if the file has expired
    if datetime.utcnow() > file_record.expires_at:
        abort(410)  # 410 Gone indicates that the resource is no longer available and will not be available again.

    # Build the filepath using the UPLOAD_FOLDER setting and the unique file identifier
    filepath = os.path.join(UPLOADS_FOLDER, unique_id)

    # Check if the file exists in the filesystem
    if not os.path.isfile(filepath):
        abort(404)  # 404 Not Found if the file does not exist on the server

    # Increment the download_count by 1
    file_record.download_count += 1
    db.session.commit()

    # Serve the file for download, using the original filename for the download
    return send_from_directory(directory=UPLOADS_FOLDER,
                               path=unique_id,
                               as_attachment=True,
                               download_name=file_record.filename)


@file_routes.route('/upload/success/<unique_id>')
def upload_success(unique_id):
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    file_details = {
        'url': url_for('file_routes.download_file_page', unique_id=unique_id, _external=True),
        'filename': file_record.filename,
        'message': file_record.message,
        'expires_at': file_record.expires_at,
        'download_link': url_for('direct_download_file', unique_id=unique_id, _external=True),
        'download_count': file_record.download_count
    }
    return render_template('upload_success.html',
                           file=file_details,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)
