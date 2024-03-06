from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, login_user, current_user
from flask import jsonify
from ..models.user import User
from ..models.file import File
from ..db import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email

from . import file_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package

user_routes = Blueprint('user_routes', __name__)


class SignUpForm(FlaskForm):
    """
    Sign-up user form
    """
    name = StringField("Enter name:",
                       validators=[DataRequired()])
    email = EmailField("Enter email: ",
                       validators=[DataRequired(), Email()])
    password = PasswordField("Enter password: ",
                             validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """
    Login user form
    """
    email = EmailField("Enter email: ",
                       validators=[DataRequired(), Email()])
    password = PasswordField("Enter password: ",
                             validators=[DataRequired()])
    submit = SubmitField("Submit")


@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''

        email_check = User.query.filter_by(email=email).first()  # Check if email already taken
        if email_check:
            flash('Email already exists.', 'warning')
            return redirect(url_for('user_routes.signup'))

        new_user = User(name=name, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('user_routes.login'))
    return render_template('signup.html',
                           form=form,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user, remember=True)
            if 'PyQt' in request.headers.get('User-Agent'):
                # For PyQt application, send a JSON response indicating login was successful
                return jsonify({
                    'success': True,
                    'message': "Login successful!",
                    'redirect': url_for('user_routes.profile', _external=True)  # Provide the URL for PyQt to navigate
                })
            else:
                # For web browsers, redirect to the profile page
                flash("Login successful!", 'success')
                return redirect(url_for('user_routes.profile'))
        else:
            flash("Incorrect credentials - Try again", 'error')

    if 'PyQt' in request.headers.get('User-Agent'):
        # For PyQt application, optionally render a specific template or return JSON indicating to show the login page
        return jsonify({
            'success': False,
            'message': "Show login page",
            'redirect': url_for('user_routes.login_pyqt_template', _external=True)  # Assuming there's a route for PyQt login template
        })
    else:
        # For web browsers, render the standard login template
        return render_template('login.html', form=form, user_routes=user_routes, file_routes=file_routes, main_routes=main_routes)


@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", 'success')
    return redirect(url_for('main_routes.home'))


@user_routes.route('/profile', methods=['GET'])
@login_required
def profile():
    user_files = User.query.get(current_user.id).files
    return render_template('profile.html',
                           user_files=user_files,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


# TODO: Delete account functionality
@user_routes.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    # user = User.query.get(current_user.id)
    # if request.method == 'POST':
    #     db.session.delete(user)
    #     db.session.commit()
    #     flash("Account deleted successfully", 'success')
    #     return redirect(url_for('main_routes.home'))
    # return render_template('delete_account.html',
    #                        user_routes=user_routes,
    #                        file_routes=file_routes,
    #                        main_routes=main_routes)
    pass


# TODO: Update account functionality
@user_routes.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    pass
