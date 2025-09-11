# Configuration module for Portfolio Analyzer - loads database and app settings from environment variables
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

# Root database config for setup operations
DB_ROOT_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_ROOT_USER', 'root'),
    'password': os.getenv('DB_ROOT_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

SECRET_KEY = os.getenv('SECRET_KEY')

# Admin user configuration
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')