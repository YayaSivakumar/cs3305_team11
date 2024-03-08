from . import user_routes  # Import Blueprint instance from the main application package
from . import main_routes  # Import Blueprint instance from the main application package
from . import file_routes  # Import Blueprint instance from the main application package

from flask import Blueprint, render_template

# Define a blueprint
errors_routes = Blueprint('errors_route', __name__, template_folder='templates')


# Define custom error handlers
@errors_routes.app_errorhandler(404)
def page_not_found(error):
    """
    Custom error handler for 404 errors
    """
    return render_template('404.html',
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes), 404


@errors_routes.app_errorhandler(500)
def internal_server_error(error):
    """
        Custom error handler for 500 errors
    """
    return render_template('500.html',
                           user_routes=user_routes,
                           file_routes=file_routes,
                           main_routes=main_routes), 500


# You can add more error handlers as needed

# Register the blueprint with the application

