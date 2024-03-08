from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, login_user, current_user

from ..models.user import User
from ..models.file_upload import File
from ..models.file_upload import Upload

from ..db import db

from ..forms.user_forms import SignUpForm, LoginForm

from . import file_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

# Define a Blueprint for the user routes
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        # If the user is already logged in, redirect to the profile page
        return redirect(url_for('user_routes.profile'))
    # Create a new instance of the signup form
    form = SignUpForm()
    if form.validate_on_submit():
        # Get form data
        name = form.name.data
        form.name.data = ''
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''
        # Check if the email is already taken
        email_check = User.query.filter_by(email=email).first()  # Check if email already taken
        if email_check:
            # If the email is already taken, redirect to the signup page
            flash('Email already exists.', 'warning')
            return redirect(url_for('user_routes.signup'))
        # Create a new user
        new_user = User(name=name, email=email)
        # Set the password for this new user
        new_user.password = password
        # Add the new user to the database
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('user_routes.login'))

    return render_template('signup.html',
                           form=form,
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log the user in
    """
    if current_user.is_authenticated:
        # If the user is already logged in, redirect to the profile page
        return redirect(url_for('user_routes.profile'))
    # Create a new instance of the login form
    form = LoginForm()
    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user, remember=True)
            flash("Login successful!", 'success')
            return redirect(url_for(f'user_routes.profile'))
        else:
            flash("Incorrect credentials - Try again", 'error')

    else:
        return render_template('login.html',
                               form=form,
                               is_pyqt='PyQt' in request.headers.get('User-Agent'),
                               user_routes=user_routes,
                               file_routes=file_routes,
                               main_routes=main_routes)


@user_routes.route('/logout')
@login_required
def logout():
    """
    Log the current user out
    """
    logout_user()
    flash("You have been logged out", 'success')
    return redirect(url_for('main_routes.home'))


@user_routes.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    Render the profile page
    """
    # Get all the uploads for the current user
    user_uploads = current_user.uploads
    return render_template('profile.html',
                           is_pyqt='PyQt' in request.headers.get('User-Agent'),
                           user_uploads=user_uploads,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)
