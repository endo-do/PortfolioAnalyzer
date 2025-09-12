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
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@portfolioanalyzer.com')

# Network configuration
HOST_IP = os.getenv('HOST_IP', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DB_PORT = int(os.getenv('DB_PORT', 3306))

# Timezone configuration
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# Database connection pool configuration
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))
DB_POOL_NAME = os.getenv('DB_POOL_NAME', 'mypool')

# Logging configuration
LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10 * 1024 * 1024))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
SECURITY_LOG_MAX_BYTES = int(os.getenv('SECURITY_LOG_MAX_BYTES', 5 * 1024 * 1024))  # 5MB
SECURITY_LOG_BACKUP_COUNT = int(os.getenv('SECURITY_LOG_BACKUP_COUNT', 10))
ERROR_LOG_MAX_BYTES = int(os.getenv('ERROR_LOG_MAX_BYTES', 5 * 1024 * 1024))  # 5MB
ERROR_LOG_BACKUP_COUNT = int(os.getenv('ERROR_LOG_BACKUP_COUNT', 5))

# Password validation configuration
PASSWORD_MAX_LENGTH = int(os.getenv('PASSWORD_MAX_LENGTH', 128))
PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))

# Form validation limits
PORTFOLIO_NAME_MAX_LENGTH = int(os.getenv('PORTFOLIO_NAME_MAX_LENGTH', 50))
PORTFOLIO_DESCRIPTION_MAX_LENGTH = int(os.getenv('PORTFOLIO_DESCRIPTION_MAX_LENGTH', 255))
BOND_SYMBOL_MAX_LENGTH = int(os.getenv('BOND_SYMBOL_MAX_LENGTH', 50))
BOND_WEBSITE_MAX_LENGTH = int(os.getenv('BOND_WEBSITE_MAX_LENGTH', 100))
BOND_COUNTRY_MAX_LENGTH = int(os.getenv('BOND_COUNTRY_MAX_LENGTH', 50))
BOND_INDUSTRY_MAX_LENGTH = int(os.getenv('BOND_INDUSTRY_MAX_LENGTH', 50))
EXCHANGE_NAME_MAX_LENGTH = int(os.getenv('EXCHANGE_NAME_MAX_LENGTH', 255))
CURRENCY_NAME_MAX_LENGTH = int(os.getenv('CURRENCY_NAME_MAX_LENGTH', 50))
CURRENCY_CODE_MAX_LENGTH = int(os.getenv('CURRENCY_CODE_MAX_LENGTH', 3))
CURRENCY_SYMBOL_MAX_LENGTH = int(os.getenv('CURRENCY_SYMBOL_MAX_LENGTH', 10))

# API configuration
YAHOO_FINANCE_PERIOD_DAYS = int(os.getenv('YAHOO_FINANCE_PERIOD_DAYS', 5))
YAHOO_FINANCE_EXCHANGE_PERIOD_DAYS = int(os.getenv('YAHOO_FINANCE_EXCHANGE_PERIOD_DAYS', 1))
YAHOO_FINANCE_INFO_PERIOD_DAYS = int(os.getenv('YAHOO_FINANCE_INFO_PERIOD_DAYS', 1))
YAHOO_FINANCE_LOOKUP_PERIOD_DAYS = int(os.getenv('YAHOO_FINANCE_LOOKUP_PERIOD_DAYS', 7))

# Scheduler configuration
SCHEDULER_HOUR = int(os.getenv('SCHEDULER_HOUR', 0))
SCHEDULER_MINUTE = int(os.getenv('SCHEDULER_MINUTE', 0))

# Timeout configuration
API_TIMEOUT_SECONDS = int(os.getenv('API_TIMEOUT_SECONDS', 15))
UI_TIMEOUT_MS = int(os.getenv('UI_TIMEOUT_MS', 5000))
UI_UPDATE_DELAY_MS = int(os.getenv('UI_UPDATE_DELAY_MS', 10))

# External URLs
YAHOO_FINANCE_BASE_URL = os.getenv('YAHOO_FINANCE_BASE_URL', 'https://finance.yahoo.com')
YAHOO_FINANCE_QUOTE_URL = os.getenv('YAHOO_FINANCE_QUOTE_URL', 'https://finance.yahoo.com/quote/')
YAHOO_FINANCE_LOOKUP_URL = os.getenv('YAHOO_FINANCE_LOOKUP_URL', 'https://finance.yahoo.com/lookup?s=')

# CDN URLs
BOOTSTRAP_CSS_URL = os.getenv('BOOTSTRAP_CSS_URL', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css')
BOOTSTRAP_JS_URL = os.getenv('BOOTSTRAP_JS_URL', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js')
FONT_AWESOME_CSS_URL = os.getenv('FONT_AWESOME_CSS_URL', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css')
CHART_JS_URL = os.getenv('CHART_JS_URL', 'https://cdn.jsdelivr.net/npm/chart.js')
CHART_JS_DATALABELS_URL = os.getenv('CHART_JS_DATALABELS_URL', 'https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2')

# Docker configuration
GUNICORN_WORKERS = int(os.getenv('GUNICORN_WORKERS', 4))
GUNICORN_BIND = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')

# Health check configuration
DB_HEALTH_CHECK_INTERVAL = int(os.getenv('DB_HEALTH_CHECK_INTERVAL', 10))
DB_HEALTH_CHECK_TIMEOUT = int(os.getenv('DB_HEALTH_CHECK_TIMEOUT', 5))
DB_HEALTH_CHECK_RETRIES = int(os.getenv('DB_HEALTH_CHECK_RETRIES', 5))
DB_HEALTH_CHECK_START_PERIOD = int(os.getenv('DB_HEALTH_CHECK_START_PERIOD', 30))
WEB_HEALTH_CHECK_INTERVAL = int(os.getenv('WEB_HEALTH_CHECK_INTERVAL', 30))
WEB_HEALTH_CHECK_TIMEOUT = int(os.getenv('WEB_HEALTH_CHECK_TIMEOUT', 10))
WEB_HEALTH_CHECK_RETRIES = int(os.getenv('WEB_HEALTH_CHECK_RETRIES', 3))
WEB_HEALTH_CHECK_START_PERIOD = int(os.getenv('WEB_HEALTH_CHECK_START_PERIOD', 40))