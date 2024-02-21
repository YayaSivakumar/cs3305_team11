
# Import individual route files to register Blueprints
from .main_routes import main_routes
from .file_routes import file_routes
from .user_routes import user_routes

# Initialize and register Blueprints
def register_routes(app):
    app.register_blueprint(main_routes)
    app.register_blueprint(file_routes)
    app.register_blueprint(user_routes)
