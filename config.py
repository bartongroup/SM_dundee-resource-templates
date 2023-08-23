import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_PATH = os.path.join(BASE_DIR, 'uploads')
UPLOAD_PATH = os.environ.get('APP_UPLOAD_PATH', UPLOAD_PATH)

DOWNLOAD_PATH = os.path.join(BASE_DIR, 'download')
DOWNLOAD_PATH = os.environ.get('APP_DOWNLOAD_PATH', DOWNLOAD_PATH)

DEFAULT_LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_PATH = os.environ.get('APP_LOG_PATH', DEFAULT_LOG_PATH)

DEFAULT_DATABASE_PATH = os.path.join(BASE_DIR, 'db', 'session.db')
DATABASE_PATH = os.environ.get('APP_DATABASE_PATH', DEFAULT_DATABASE_PATH)