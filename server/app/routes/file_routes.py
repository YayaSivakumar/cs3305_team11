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

from ..models.file import File
from ..models.user import User

from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

file_routes = Blueprint('file_routes', __name__)


# TODO: Make a Forms folder and move all forms there
class UploadForm(FlaskForm):
    """
    File upload form
    """
    # TODO: Add an optional field to add a name
    message = TextAreaField("Enter message: ")
    file_name = StringField("Enter file name: ")
    expiration_hours = SelectField("Enter expiration hours: ",
                                   choices=[('24 Hours', '24'), ('3 Days', '72'), ('7 Days', '168')],
                                   default='24 Hours',
                                   validators=[DataRequired()])
    file = MultipleFileField("Choose file: ",
                             validators=[DataRequired()])
    password = PasswordField("Enter password: ")
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    """
    File update form
    """
    message = StringField("Enter message: ")
    expiration_hours = StringField("Enter expiration hours: ",
                                   validators=[DataRequired()])
    submit = SubmitField("Submit")


@file_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    This function handles file uploads. It accepts POST requests with a file, message, expiration_hours,
    and password fields.
    """
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            message = form.message.data
            form.message.data = ''
            password = form.password.data
            form.password.data = ''
            expiration_hours = form.expiration_hours.data
            filename = form.file_name.data
            form.file_name.data = ''
            # List of filenames could be used to represent multiple files on download page
            #     Maybe optional toggle in upload form?
            files_filenames = []
            files = []
            for uploaded_file in form.file.data:
                if uploaded_file:
                    print(f"Uploaded file: {uploaded_file}, Type: {type(uploaded_file)}")
                    filename = secure_filename(uploaded_file.filename)
                    files_filenames.append(filename)
                    files.append(uploaded_file)
            #         should we compress files pre upload aswell?
            unique_id = str(uuid.uuid4())
            expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
            if not filename:
                filename = f"{current_user.name}_file_upload{unique_id[:6]}"
            filepath = os.path.join(UPLOADS_FOLDER, unique_id)
            if len(files_filenames) > 1:
                # ZIP FILES HERE
                compressed_file = compress_dir(files, filename)
                # compress_dir returns the filepath to the compressed file
                with open(compressed_file, 'rb') as file:
                    werkzeug_file = FileStorage(
                        stream=file,
                        filename=filename,
                        content_type='application/zip',
                    )
                    werkzeug_file.save(filepath)
            #     if compressed_file has
            # else:
            #     uploaded_file.save(filepath)

            new_file = File(filename=filename, unique_id=unique_id, message=message, expires_at=expires_at)
            new_file.password = password
            current_user.files.append(new_file)
            db.session.add(new_file)
            db.session.commit()
            link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
            flash('File uploaded successfully.', 'success')
            return redirect(url_for('file_routes.upload_success', unique_id=unique_id))
    else:
        # If it's not a POST request, just render the template without context
        return render_template('upload.html',
                               form=form,
                               user_routes=user_routes,
                               file_routes=file_routes,
                               main_routes=main_routes)


@file_routes.route('/upload_dan', methods=['GET', 'POST'])
@login_required
def upload_dan():
    """
    This function handles file uploads. It accepts POST requests with a file, message, expiration_hours,
    and password fields.
    """
    if request.method == 'POST':
        message = request.form.get('message', '')
        expiration_hours = int(request.form.get('expiration_hours', 24))
        uploaded_files = request.files.getlist('file')  # Get the list of files

        upload_responses = []
        for file in uploaded_files:
            if file:
                print(f"Uploaded file: {file}, Type: {type(file)}")
                filename = secure_filename(file.filename)
                unique_id = str(uuid.uuid4())
                filepath = os.path.join(UPLOADS_FOLDER, unique_id)
                file.save(filepath)
                expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
                new_file = File(filename=filename, unique_id=unique_id, message=message, expires_at=expires_at)

                current_user.files.append(new_file)
                db.session.add(new_file)
                db.session.commit()

                link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
                upload_responses.append({'filename': filename, 'link': link})

        if 'PyQt' in request.headers.get('User-Agent'):
            # Return a JSON response for the PyQt application with all the upload responses
            return jsonify({
                'success': True,
                'message': 'Files uploaded successfully.',
                'files': upload_responses
            })

        flash('Files uploaded successfully.', 'success')
        # Redirect to a page that can handle showing multiple upload successes
        return redirect(url_for('file_routes.upload_success', unique_id=unique_id))

    # For GET requests, render the upload form template
    return render_template('upload_dan.html',
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/upload_success/<unique_id>', methods=['GET'])
@login_required
def upload_success(unique_id):
    file_info = File.query.filter_by(unique_id=unique_id).first_or_404()
    link = url_for('file_routes.download_file_page', unique_id=unique_id, _external=True)
    file_user_id = file_info.user_id
    file_user_details = User.query.get(file_user_id)
    file_info = {
        'filename': file_info.filename,
        'message': file_info.message,
        'expires_at': file_info.expires_at,
        'download_link': link,
        'upload_user': file_user_details
    }
    return render_template('upload_success.html',
                           link=link,
                           file_info=file_info,
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


@file_routes.route('/update_file/<unique_id>', methods=['GET', 'POST'])
@login_required
def update_file(unique_id):
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    if request.method == 'POST':
        message = request.form.get('message', '')
        expiration_hours = int(request.form.get('expiration_hours', 24))

        file_record.message = message
        file_record.expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
        db.session.commit()

        flash("File updated successfully", 'success')
        return redirect(url_for('user_routes.profile'))
    return render_template('update_file.html',
                           file=file_record,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/delete_file/<unique_id>', methods=['GET', 'POST'])
@login_required
def delete_file(unique_id):
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    print(f"File: {file_record.filename}")
    if request.method == 'POST':
        db.session.delete(file_record)
        db.session.commit()

        flash("File deleted successfully", 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('delete_file.html',
                           file=file_record,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/download/<unique_id>', methods=['GET'])
def download_file_page(unique_id):
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    file_user_id = file_record.user_id
    file_user_details = User.query.get(file_user_id)

    file_details = {
        'filename': file_record.filename,
        'message': file_record.message,
        'expires_at': file_record.expires_at,
        'download_link': url_for('file_routes.direct_download_file',
                                 unique_id=unique_id,
                                 _external=True),
        'upload_user': file_user_details
    }

    return render_template('download.html',
                           file=file_details,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@file_routes.route('/download/file/<unique_id>', methods=['GET'])
def direct_download_file(unique_id):
    # Fetch the file record using the unique ID from the database
    print("Making file record")
    print("Unique ID: ", unique_id)
    file_record = File.query.filter_by(unique_id=unique_id).first_or_404()
    print("File record made")
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
