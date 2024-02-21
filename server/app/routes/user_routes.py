from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash
from ..models.user import User
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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hashed, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('main.home'))  # if user doesn't exist or password is wrong, reload the page
        login_user(user)  # Log in the user
        return redirect(url_for('main.home'))
    else:
        name = None
        email = None
        password = None
        form = LoginForm()
        return render_template('login.html',
                               form=form,
                               file_routes=file_routes,
                               user_routes=user_routes,
                               main_routes=main_routes)


@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
