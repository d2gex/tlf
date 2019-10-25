import os

from pathlib import Path
from dotenv import load_dotenv
from os.path import join


path = Path(__file__).resolve()
ROOT_PATH = str(path.parents[1])
dot_env = load_dotenv(join(ROOT_PATH, '.env'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_SETTINGS = {
        'host': os.getenv('DB_HOST'),
        'db': os.getenv('DB'),
        'port': int(os.getenv('DB_PORT')),
        'username': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'authentication_source': os.getenv('DB_AUTH_SOURCE')
    }
