# WSGI entry point for Portfolio Analyzer - creates Flask app instance for production deployment
from app import create_app
app = create_app()