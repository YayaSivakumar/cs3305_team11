from flask import Blueprint, render_template

from . import user_routes  # Import Blueprint instance from the main application package
from . import file_routes  # Import Blueprint instance from the main application package

main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def home():
    return render_template('index.html',
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


@main_routes.route('/about')
def about():
    pass


@main_routes.route('/install')
def install_package():
    '''
    install python package
    '''
    pass
