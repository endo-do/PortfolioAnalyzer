"""Loads database and secret key configuration from environment variables."""

import os
from dotenv import load_dotenv


load_dotenv()  # Load from .env file

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

SECRET_KEY = os.getenv('SECRET_KEY')