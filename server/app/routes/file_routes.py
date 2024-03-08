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

from ..models.file_upload import File, Upload
from ..models.user import User

from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

from ..forms.file_forms import UploadForm, DownloadForm, UpdateForm

import zipfile

# Create a Blueprint for the file routes
file_routes = Blueprint('file_routes', __name__)


@file_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    This function handles file uploads. It accepts POST requests with files (one or many), an upload name, a message,
    expiration_hours, an optional password that means the upload will be password protected.
    """
    form = UploadForm()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')
        # Check if the form is valid
        if form.validate_on_submit():
            # Get the form data
            message = form.message.data
            form.message.data = ''
            expiration_hours = form.expiration_hours.data
            upload_name = form.upload_name.data
            form.upload_name.data = ''
            password = form.password.data
            form.password.data = ''
            # Generate a unique ID for the upload
            upload_unique_id = str(uuid.uuid4())
            # Calculate the expiration time
            expires_at = datetime.utcnow() + timedelta(hours=int(expiration_hours))
            # Create a new Upload instance
            upload_obj = Upload(user_id=current_user.id,
                                unique_id=upload_unique_id,
                                upload_name=upload_name,
                                expires_at=expires_at,
                                message=message)
            print('Upload object created')
            if password:
                # If a password was provided, add it to the upload object
                upload_obj.password = password  # Upload object has receives passwords in this way to be hashed
                print('Added password to upload_object')
            db.session.add(upload_obj)  # Add the upload object to the session
            db.session.commit()  # Commit the session to the database

            for uploaded_file in uploaded_files:
                # Now we want to track what is inside the upload, what are the files
                if uploaded_file:
                    filename = secure_filename(uploaded_file.filename)  # Secure the filename, sanitisation!
                    unique_id = str(uuid.uuid4()) # Generate a unique ID for each file
                    # Create a filepath for the file using the unique ID
                    filepath = os.path.join(UPLOADS_FOLDER, unique_id)
                    uploaded_file.save(filepath)

                    # Keep same expiration time for all files in the upload

                    # Create a new File instance and associate it with the upload
                    file = File(filename=filename, unique_id=unique_id, expires_at=expires_at, upload_id=upload_obj.id)
                    # Add the file to the session
                    db.session.add(file)
                    print('File added to session')
            # Commit the session to the database, saving the files
            db.session.commit()
            flash('Upload completed successfully.', 'success')
            return redirect(url_for('file_routes.upload_success', unique_id=upload_obj.unique_id))
        flash('Form validation failed.', 'error')
    return render_template('upload.html',
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           form=form,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/upload_success/<unique_id>', methods=['GET'])
@login_required
def upload_success(unique_id):
    """
    This function returns a page with the upload information and a link to download the files.
    """
    # Get the upload information from the database
    upload_info = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    # Generate a download link for the upload, using the unique ID of the upload
    link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
    # Get the user details of the user who uploaded the file
    upload_user_id = upload_info.user_id
    # Get the user details of the user who uploaded the file
    user_user_details = User.query.get(upload_user_id)
    upload_info = {
        'upload_name': upload_info.upload_name,
        'message': upload_info.message,
        'expires_at': upload_info.expires_at,
        'upload_user': user_user_details
    }
    return render_template('upload_success.html',
                           link=link,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           upload_info=upload_info,
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


@file_routes.route('/update_upload/<unique_id>', methods=['GET', 'POST'])
@login_required
def update_upload(unique_id):
    """
    This function updates the upload information in the database.
    On GET requests, it returns a page with a form to update the upload information.
    On POST requests, it takes the new upload name, a message, and expiration time.
    """

    # Get the upload information from the database
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    if current_user.id != upload_record.user_id:
        # Make sure the user trying to update the upload, is the owner of it
        flash("You don't have permission to update this upload", 'error')
        return redirect(url_for('main_routes.home'))
    # Create a form instance
    form = UpdateForm()
    #
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the form data
            message = form.message.data
            form.message.data = ''
            upload_name = form.upload_name.data
            form.upload_name.data = ''
            expiration_hours = form.expiration_hours.data
            # Update the upload information in the database
            upload_record.upload_name = upload_name
            upload_record.message = message
            upload_record.expires_at = datetime.utcnow() + timedelta(hours=int(expiration_hours))
            # Commit the session to the database
            db.session.commit()

            flash("File updated successfully", 'success')
            return redirect(url_for('user_routes.profile'))
        flash("Form validation failed", 'error')

    return render_template('update_upload.html',
                           upload=upload_record,
                           form=form,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/delete_upload/<unique_id>', methods=['GET', 'POST'])
@login_required
def delete_upload(unique_id):
    """
    This function deletes the upload and all its files from the database and the server.
    It being protected by the login_required decorator, it will only be accessible to logged-in users.
    """
    # Get the upload information from the database
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    if current_user.id != upload_record.user_id:
        # Make sure the user trying to delete the upload, is the owner of it
        flash("You don't have permission to delete this upload", 'error')
        return redirect(url_for('main_routes.home'))
    print(f"Upload: {upload_record.upload_name}")
    if request.method == 'POST':
            # Delete the files from the server
        for file in upload_record.files:
            file_path = os.path.join(UPLOADS_FOLDER, file.unique_id)
            if os.path.isfile(file_path):
                os.remove(file_path)
        db.session.delete(upload_record)
        # Commit the session to the database
        db.session.commit()

        flash("Upload deleted successfully", 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('delete_upload.html',
                           file=upload_record,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/download/<unique_id>', methods=['GET', 'POST'])
def download_file_page(unique_id):
    """
    On GET, returns a page with the upload information and a form to download the files.
    On POST, it checks if the password is correct (if applicable) and serves the file for download.
    """
    # Get the upload information from the database
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    upload_user_id = upload_record.user_id
    upload_user_details = User.query.get(upload_user_id)
    # Create a form instance
    form = DownloadForm()

    if request.method == 'POST':
        # If the upload is password protected, check if the password is correct
        if upload_record.is_password_protected():
            # Get the password from the form
            password = form.password.data
            form.password.data = ''
            # Verify the password
            if upload_record.verify_password(password):
                # Password is correct, allow the user to download the file
                return direct_download_file(upload_record)
            else:
                # Password is incorrect, display an error message
                flash('Invalid password. Please try again.', 'error')
        else:
            # If the upload is not password protected, allow the user to download the file
            return direct_download_file(upload_record)
    upload_details = {
        'filename': upload_record.upload_name,
        'message': upload_record.message,
        'expires_at': upload_record.expires_at,
        'unique_id': unique_id,
        'is_password_protected': upload_record.is_password_protected(),
        'upload_user': upload_user_details
    }

    return render_template('download.html',
                           form=form,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           upload=upload_details,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


def direct_download_file(upload_record):
    """
    Function to serve the upload for download
    behaves differently if the upload contains one or multiple files
    """
    if datetime.utcnow() > upload_record.expires_at:
        # If the upload has expired, return a 410 Gone response
        abort(410)

    if upload_record.upload_name:
        # If the upload has a name given by uploader, use it as the download name
        upload_name = secure_filename(upload_record.upload_name)
    else:
        # Otherwise, use the name of the user who uploaded the file with a piece of the unique ID
        upload_name = f"{current_user.name}_file_upload_{upload_record.unique_id[:6]}"

    if len(upload_record.files) > 1:
        # if more than one file in the upload, compress the files into a zip archive
        # Create a zip archive containing all files in the upload
        zip_filepath = os.path.join(UPLOADS_FOLDER, f"{upload_record.unique_id}.zip")
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            # Add each file to the zip archive
            for file in upload_record.files:
                file_path = str(os.path.join(UPLOADS_FOLDER, file.unique_id))
                zipf.write(file_path, arcname=file.filename)

        # Increment the download_count of the upload by 1
        upload_record.download_count += 1
        db.session.commit()

        # Serve the zip file for download
        return send_from_directory(directory=UPLOADS_FOLDER,
                                   path=f"{upload_record.unique_id}.zip",
                                   as_attachment=True,
                                   download_name=f"{upload_name}.zip")
    else:
        # Serve the single file for download
        file_record = upload_record.files[0]
        filepath = os.path.join(UPLOADS_FOLDER, file_record.unique_id)
        if not os.path.isfile(filepath):
            # If the file doesn't exist, return a 404 Not Found response
            abort(404)

        # Increment the download_count of the upload by 1
        upload_record.download_count += 1
        db.session.commit()

        return send_from_directory(directory=UPLOADS_FOLDER,
                                   path=file_record.unique_id,
                                   as_attachment=True,
                                   download_name=file_record.filename)

