import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SESSIONS_FOLDER = os.path.join(BASE_DIR, 'sessions')
SESSIONS_FOLDER = os.environ.get('APP_SESSIONS_PATH', SESSIONS_FOLDER)

LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_PATH = os.environ.get('APP_LOG_PATH', LOG_PATH)

DATABASE_PATH = os.path.join(BASE_DIR, 'db', 'session.sqlite')
DATABASE_PATH = os.environ.get('APP_DATABASE_PATH', DATABASE_PATH)

SLIVKA_URL = os.environ.get('SLIVKA_URL', 'http://localhost:8000/')