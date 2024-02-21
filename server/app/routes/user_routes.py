from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash
from ..models.user import User
from ..db import db

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()  # Check if user already exists
        if user:
            flash('Email address already exists')
            return redirect(url_for('main.home'))
        new_user = User(email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.home'))
    else:
        return render_template('sign_up.html')


@user_routes.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hashed, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.home'))  # if user doesn't exist or password is wrong, reload the page
    login_user(user)  # Log in the user
    return redirect(url_for('main.home'))


@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
