"""
Test configuration and fixtures for Portfolio Analyzer tests.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from werkzeug.security import generate_password_hash

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database.connection.pool import get_db_connection

@pytest.fixture(scope='session')
def app():
    """Create and configure a test Flask application."""
    # Create test app with test configuration
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'LOGIN_DISABLED': False,
    })
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    def _auth_headers(username='testuser', password='TestPass123!'):
        # Register user first
        client.post('/auth/register', data={
            'username': username,
            'userpwd': password,
            'confirm_password': password
        })
        
        # Login and get session
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        })
        
        # Return headers with session cookie
        return {
            'Cookie': response.headers.get('Set-Cookie', '')
        }
    return _auth_headers

@pytest.fixture
def admin_headers(client):
    """Create admin authentication headers for testing."""
    def _admin_headers(username='admin', password='admin'):
        # Try to create admin user, but handle if it already exists
        try:
            from app.database.tables.user.create_default_admin_user import create_default_admin_user
            create_default_admin_user()
        except Exception:
            # Admin user already exists, that's fine
            pass
        
        # Login as admin
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        })
        
        return {
            'Cookie': response.headers.get('Set-Cookie', '')
        }
    return _admin_headers

@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing."""
    with patch('app.database.connection.pool.get_db_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        yield mock_conn

@pytest.fixture
def mock_yfinance():
    """Mock yfinance API calls."""
    with patch('yfinance.Ticker') as mock_ticker:
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Mock successful price data
        mock_ticker_instance.history.return_value = MagicMock()
        mock_ticker_instance.history.return_value.empty = False
        mock_ticker_instance.history.return_value.iloc = [MagicMock()]
        mock_ticker_instance.history.return_value.iloc[0].Close = 100.50
        
        yield mock_ticker

@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing."""
    return {
        'portfolioname': 'Test Portfolio',
        'portfoliodescription': 'A test portfolio for unit testing',
        'currencycode': 'USD'
    }

@pytest.fixture
def sample_bond_data():
    """Sample bond data for testing."""
    return {
        'bondname': 'Test Bond',
        'bondsymbol': 'TEST',
        'bondcategoryid': 1,
        'bondcurrencyid': 1,
        'bondsector': 'Technology',
        'exchangeid': 1
    }

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'username': 'testuser',
        'userpwd': 'TestPass123!',
        'confirm_password': 'TestPass123!'
    }

@pytest.fixture
def sample_currency_data():
    """Sample currency data for testing."""
    return {
        'currencycode': 'EUR',
        'currencyname': 'Euro'
    }

@pytest.fixture
def sample_exchange_data():
    """Sample exchange data for testing."""
    return {
        'exchangesymbol': 'NYSE',
        'exchangename': 'New York Stock Exchange',
        'regionid': 1
    }

@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files after each test."""
    yield
    # Clean up test log files
    log_files = ['test_app.log', 'test_security.log', 'test_errors.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except PermissionError:
                # File is locked, skip cleanup
                pass

@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Clean up test data after each test."""
    yield
    # Clean up any test-specific data if needed
    # This can be expanded based on specific test requirements

@pytest.fixture
def mock_logger():
    """Mock the logging system for testing."""
    with patch('app.utils.logger.log_user_action') as mock_user_action, \
         patch('app.utils.logger.log_security_event') as mock_security, \
         patch('app.utils.logger.log_error') as mock_error:
        yield {
            'user_action': mock_user_action,
            'security': mock_security,
            'error': mock_error
        }
