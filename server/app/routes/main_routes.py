from flask import Blueprint, render_template

main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def home():
    return render_template('index.html')


@main_routes.route('/about')
def about():
    pass


@main_routes.route('/install')
def install_package():
    '''
    install python package
    '''
    pass
