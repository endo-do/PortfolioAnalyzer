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
from tests.test_config import get_test_db_config
from tests.database_setup import create_test_database, setup_test_database, cleanup_test_database

@pytest.fixture(scope='session')
def test_database():
    """Set up and tear down test database for the entire test session."""
    # Create and set up test database
    print("🔧 Setting up test database...")
    create_test_database()
    setup_test_database()
    
    yield
    
    # Clean up test database after all tests
    print("🧹 Cleaning up test database...")
    cleanup_test_database()

@pytest.fixture(scope='session')
def app(test_database):
    """Create and configure a test Flask application."""
    # Override database configuration for testing
    import config
    from app.database.connection import pool
    
    test_config = get_test_db_config()
    
    # Store original config and pool
    original_config = config.DB_CONFIG.copy()
    original_pool = pool.connection_pool
    
    # Set test database config
    config.DB_CONFIG.update(test_config)
    pool.connection_pool = None  # Force reinitialization with test config
    
    # Create test app with test configuration
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'LOGIN_DISABLED': False,
    })
    
    with app.app_context():
        yield app
    
    # Restore original config and pool
    config.DB_CONFIG.update(original_config)
    pool.connection_pool = original_pool

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    client = app.test_client()
    # Set User-Agent to indicate this is a test client
    client.environ_base['HTTP_USER_AGENT'] = 'pytest-test-client'
    return client

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    def _auth_headers(username='testuser', password='MySecurePass1!'):
        # Register user first
        client.post('/auth/register', data={
            'username': username,
            'userpwd': password,
            'userpwd_confirm': password
        })
        
        # Login and get session - follow redirects to maintain session
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        }, follow_redirects=True)
        
        # Return headers with session cookie - handle both Set-Cookie and session
        headers = {}
        if 'Set-Cookie' in response.headers:
            headers['Cookie'] = response.headers.get('Set-Cookie', '')
        
        return headers
    return _auth_headers

@pytest.fixture
def authenticated_client(client):
    """Create an authenticated test client."""
    def _authenticated_client(username='testuser', password='MySecurePass1!'):
        # Register user first
        client.post('/auth/register', data={
            'username': username,
            'userpwd': password,
            'userpwd_confirm': password
        })
        
        # Login and maintain session
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        }, follow_redirects=True)
        
        # Ensure session is maintained
        with client.session_transaction() as sess:
            sess['_fresh'] = True
        
        return client
    return _authenticated_client

@pytest.fixture
def admin_client(client):
    """Create an admin-authenticated test client."""
    def _admin_client(username='admin', password='admin'):
        # Login as admin and maintain session
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        }, follow_redirects=True)
        
        # Ensure session is maintained
        with client.session_transaction() as sess:
            sess['_fresh'] = True
        
        return client
    return _admin_client

@pytest.fixture
def admin_headers(client):
    """Create admin authentication headers for testing."""
    def _admin_headers(username='admin', password='admin'):
        # Don't try to create admin user - it already exists from database setup
        # Just login with the existing admin credentials
        
        # Login as admin - follow redirects to maintain session
        response = client.post('/auth/login', data={
            'username': username,
            'userpwd': password
        }, follow_redirects=True)
        
        # Return headers with session cookie - handle both Set-Cookie and session
        headers = {}
        if 'Set-Cookie' in response.headers:
            headers['Cookie'] = response.headers.get('Set-Cookie', '')
        
        return headers
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
        'userpwd': 'MySecurePass1!',
        'confirm_password': 'MySecurePass1!'
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
        'exchangename': 'NYSE',
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

@pytest.fixture
def admin_user_exists():
    """Fixture to check if admin user exists and handle creation gracefully."""
    def _check_admin_exists():
        from app.database.connection.pool import get_db_connection
        from app.database.helpers.fetch_one import fetch_one
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            result = fetch_one(cursor, "SELECT id FROM user WHERE username = 'admin'")
            return result is not None
        finally:
            cursor.close()
            conn.close()
    
    return _check_admin_exists

@pytest.fixture
def safe_admin_creation():
    """Safely create admin user only if it doesn't exist."""
    def _create_admin_if_needed():
        from app.database.tables.user.create_default_admin_user import create_default_admin_user
        try:
            create_default_admin_user()
            return True
        except Exception as e:
            # Admin user already exists or other error
            if "Duplicate entry" in str(e):
                return False  # Already exists
            else:
                raise e  # Re-raise other errors
    
    return _create_admin_if_needed
