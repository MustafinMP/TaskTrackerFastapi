import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_SALT = os.environ.get('PASSWORD_SALT')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')

INVITE_LINK_SALT = os.environ.get('INVITE_LINK_SALT')
MIN_DEADLINE_GAP = timedelta(minutes=5)

YA_CLIENT_ID = os.environ.get('YA_CLIENT_ID')
YANDEX_API_REQUEST = os.environ.get('YANDEX_API_REQUEST')
YA_CLIENT_SECRET = os.environ.get('YA_CLIENT_SECRET')

HOST = 'localhost'
