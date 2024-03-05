from flask import Blueprint, render_template, request, flash, jsonify

from . import user_routes  # Import Blueprint instance from the main application package
from . import file_routes  # Import Blueprint instance from the main application package

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def home():
    return render_template('index.html',
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


@main_routes.route('/about')
def about():
    return render_template('about.html',
                           file_routes=file_routes,
                           user_routes=user_routes,
                           main_routes=main_routes)


@main_routes.route('/trigger_flash', methods=['POST'])
def trigger_flash():
    data = request.get_json()
    print(f'DATA: {data}')
    flash(data['message'], data['category'])
    return jsonify({'status': 'success'})
