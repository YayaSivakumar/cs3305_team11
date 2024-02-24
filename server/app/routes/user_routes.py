from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, login_user

from werkzeug.security import check_password_hash
# TODO: change werkzeug.security to bcrypt for File model

# TODO: Users database stuff - need delete, and update aswell
# TODO: Add user profile page, this would show all the files uploaded by the user
#  and maybe admin dashboard for this
#   TODO: need to make sure to keep simple, and not overcomplicate things, this is not core feature
from ..models.user import User
from ..db import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email

from ..login_manager import login_manager

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
    # if request.method == 'POST':
    name = None
    email = None
    password = None
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
            flash('Email already exists.')
            return redirect(url_for('user_routes.signup'))

        new_user = User(name=name, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully')
        # return redirect(url_for('main.home'))
    our_users = User.query.order_by(User.id).all()
    return render_template('signup.html',
                           form=form,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes,
                           our_users=our_users)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user, remember=True)
            flash("Login successful!")
            return redirect(url_for(f'user_routes.profile'))
        else:
            flash("Incorrect credentials - Try again")

    return render_template('login.html',
                           form=form,
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)


@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main_routes.home'))


# TODO: Why is profile not working with ID??
@user_routes.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html',
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes)

