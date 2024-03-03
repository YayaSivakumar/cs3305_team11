import os
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect
from flask import request, render_template, send_from_directory, abort, url_for, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from ..db import db
from ..config import UPLOADS_FOLDER
from flask_login import current_user

from ..models.file import File
from ..models.user import User

from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

file_routes = Blueprint('file_routes', __name__)


@file_routes.route('/upload', methods=['GET', 'POST'])
@login_required
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

            # new_file.user = db.user
            current_user.files.append(new_file)

            # new_file.password: str = password
            db.session.add(new_file)

            db.session.commit()
            link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
            flash('File uploaded successfully.', 'success')
            print(link)
            return redirect(url_for('file_routes.upload_success', unique_id=unique_id))

    else:
        # If it's not a POST request, just render the template without context
        return render_template('upload.html',
                               user_routes=user_routes,
                               file_routes=file_routes,
                               main_routes=main_routes)


# TODO: Get file_user working
@file_routes.route('/upload_success/<int:unique_id>', methods=['GET'])
@login_required
def upload_success(unique_id):
    file_info = File.query.filter_by(unique_id=unique_id).first_or_404()
    link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
    # file_user = User.query.get(unique_id).files.user
    file_info = {
        'filename': file_info.filename,
        'message': file_info.message,
        'expires_at': file_info.expires_at,
        'download_link': link,
        # 'upload_user': file_user
    }
    return render_template('upload_success.html', link=link, file_info=file_info,
                           file_routes=file_routes, user_routes=user_routes, main_routes=main_routes)


@file_routes.route('/update_file/<int:unique_id>', methods=['GET', 'POST'])
@login_required
def update_file(unique_id):
    file = File.query.get(unique_id)
    if request.method == 'POST':
        #  need to have logic here to update the file


        flash("File updated successfully", 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('update_file.html',
                           file=file,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/delete_file/<int:unique_id>', methods=['GET', 'POST'])
@login_required
def delete_file(unique_id):
    file = File.query.get(unique_id)
    if request.method == 'POST':
        db.session.delete(file)  # What does this actually do?
        #      Does this delete ref of file from user aswell? or just from the file table?
        flash("File deleted successfully", 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('delete_file.html',
                           file=file,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)





# TODO: Get the upload user DB stuff working
@file_routes.route('/download/<unique_id>', methods=['GET'])
def download_file_page(unique_id):
    print(unique_id)
    print(File.query.all())
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    # uploader = file_record.user  # Access the user who uploaded the file

    file_details = {
        'filename': file_record.filename,
        'message': file_record.message,
        'expires_at': file_record.expires_at,
        'download_link': url_for('file_routes.direct_download_file',
                                 unique_id=unique_id,
                                 _external=True),
        # 'upload_user': {
        #     'name': uploader.name,
        #     'email': uploader.email
        # }
    }

    return render_template('download.html',
                           file=file_details,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)

# TODO: Get this working again
@file_routes.route('/download/file/<unique_id>', methods=['GET'])
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
