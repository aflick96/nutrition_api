import os
from dotenv import load_dotenv

load_dotenv()

class devConfig():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    FLASK_ENV = 'dev'
    DEBUG = True
    API_KEY = 'ZfTjptjes5uPotBIG5Vj7FKETJn9C9EGjFGp8Qpv'
    SESSION_PERMANENT = False
    DB_NAME = os.environ.get('DB_NAME_DEV')
    DB_USERNAME = os.environ.get('DB_USERNAME_DEV')
    DB_PASSWORD = os.environ.get('DB_PASSWORD_DEV')
    DB_HOST = os.environ.get('DB_HOST_DEV')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class prodConfig():
    BASEDIR = os.path.abspath(os.path.dirname(__file__)) 
    FLASK_ENV = 'production'
    SESSION_PERMANENT=False
    DEBUG = False
    DB_NAME = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
