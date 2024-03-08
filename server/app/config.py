import os

"""
This file contains the configuration for the Flask app
"""

UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER')
SECRET_KEY = os.getenv('SECRET_KEY')