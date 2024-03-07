import os
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect
from flask import request, render_template, send_from_directory, abort, url_for, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from ..db import db
from ..config import UPLOADS_FOLDER
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField, MultipleFileField
from wtforms.validators import DataRequired

from python.modules.compress_dir import compress_dir

from ..models.file import File, Upload
from ..models.user import User

from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package
from ..forms.file_forms import UploadForm, DownloadForm

import zipfile

file_routes = Blueprint('file_routes', __name__)




@file_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    This function handles file uploads. It accepts POST requests with a file, message, expiration_hours,
    and password fields.
    """
    form = UploadForm()
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')
        if form.validate_on_submit():
            message = form.message.data
            form.message.data = ''
            expiration_hours = form.expiration_hours.data
            upload_name = form.upload_name.data
            form.upload_name.data = ''
            password = form.password.data
            form.password.data = ''
            upload_unique_id = str(uuid.uuid4())
            expires_at = datetime.utcnow() + timedelta(hours=int(expiration_hours))
            # Create a new Upload instance
            upload_obj = Upload(user_id=current_user.id,
                                unique_id=upload_unique_id,
                                upload_name=upload_name,
                                expires_at=expires_at,
                                message=message)
            print('Upload object created')
            if password:
                upload_obj.password = password
                print('Added password to upload_object')
            db.session.add(upload_obj)
            db.session.commit()

            for uploaded_file in uploaded_files:
                if uploaded_file:
                    filename = secure_filename(uploaded_file.filename)
                    unique_id = str(uuid.uuid4())
                    expires_at = datetime.utcnow() + timedelta(hours=int(expiration_hours))
                    filepath = os.path.join(UPLOADS_FOLDER, unique_id)
                    uploaded_file.save(filepath)

                    # Create a new File instance and associate it with the upload
                    file = File(filename=filename, unique_id=unique_id, expires_at=expires_at, upload_id=upload_obj.id)
                    db.session.add(file)
                    print('File added to session')

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
    upload_info = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
    upload_user_id = upload_info.user_id
    user_user_details = User.query.get(upload_user_id)
    upload_info = {
        'upload_name': upload_info.upload_name,
        'message': upload_info.message,
        'expires_at': upload_info.expires_at,
        'download_link': link,
        'upload_user': user_user_details
    }
    return render_template('upload_success.html',
                           link=link,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           upload_info=upload_info,
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


# TODO: update to fit upload model
@file_routes.route('/update_upload/<unique_id>', methods=['GET', 'POST'])
@login_required
def update_upload(unique_id):
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    form = UpdateForm()
    if request.method == 'POST':
        message = form.message.data
        form.message.data = ''
        upload_name = form.upload_name.data
        form.upload_name.data = ''
        expiration_hours = form.expiration_hours.data

        upload_record.upload_name = upload_name
        upload_record.message = message
        upload_record.expires_at = datetime.utcnow() + timedelta(hours=int(expiration_hours))
        db.session.commit()

        flash("File updated successfully", 'success')
        return redirect(url_for('user_routes.profile'))
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
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    print(f"Upload: {upload_record.upload_name}")
    if request.method == 'POST':
        db.session.delete(upload_record)
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
    upload_record = Upload.query.filter_by(unique_id=unique_id).first_or_404()
    upload_user_id = upload_record.user_id
    upload_user_details = User.query.get(upload_user_id)
    form = DownloadForm()
    if request.method == 'POST':
        if upload_record.is_password_protected():
            password = form.password.data
            form.password.data = ''
            print('Trying password')
            if upload_record.verify_password(password):
                # Password is correct, allow the user to download the file
                print('Password is correct')
                return direct_download_file(upload_record)
            else:
                # Password is incorrect, display an error message
                print('Password is correct')
                flash('Invalid password. Please try again.', 'error')
        else:
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
    unique_id is the upload's unique ID

    """
    print(f'Upload record: {upload_record}')
    if datetime.utcnow() > upload_record.expires_at:
        abort(410)
    if upload_record.upload_name:
        upload_name = secure_filename(upload_record.upload_name)

    else:
        upload_name = f"{current_user.name}_file_upload_{upload_record.unique_id[:6]}"

    if len(upload_record.files) > 1:
        # Create a zip archive containing all files in the upload
        zip_filepath = os.path.join(UPLOADS_FOLDER, f"{upload_record.unique_id}.zip")
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for file in upload_record.files:
                file_path = os.path.join(UPLOADS_FOLDER, file.unique_id)
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
            abort(404)

        # Increment the download_count of the upload by 1
        upload_record.download_count += 1
        db.session.commit()

        return send_from_directory(directory=UPLOADS_FOLDER,
                                   path=file_record.unique_id,
                                   as_attachment=True,
                                   download_name=file_record.filename)

