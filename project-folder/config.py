"""Flask config."""
from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask config variables."""

    ENV = 'development'
    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = environ.get('SECRET_KEY') + str(urandom(36).hex())
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # this line is to prevent SQLAlchemy from throwing a warning
    # if you don't get one with out it, feel free to remove
    SQLALCHEMY_TRACK_MODIFICATIONS = False
