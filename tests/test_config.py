"""
Test-specific configuration for Portfolio Analyzer tests.
"""

import os
import tempfile
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()

def get_test_db_config():
    """Get test database configuration from environment variables."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_ROOT_USER', 'root'),  # Use root user for tests
        'password': os.getenv('DB_ROOT_PASSWORD', ''),  # Use root password for tests
        'database': os.getenv('TEST_DB_NAME', 'portfolioanalyzer_test'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

def get_prod_db_config():
    """Get production database configuration from environment variables."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'portfolioanalyzer'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

class TestConfig:
    """Configuration for test environment."""
    
    # Test database configuration
    TEST_DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',  # Use root for tests to avoid permission issues
        'password': '',  # Will be overridden by environment variables
        'database': 'portfolioanalyzer_test',
        'port': 3306
    }
    
    # Test-specific settings
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    LOGIN_DISABLED = False
    
    # Mock external APIs
    MOCK_YFINANCE = True
    MOCK_EXTERNAL_APIS = True
    
    @classmethod
    def get_test_app_config(cls):
        """Get configuration for test Flask app."""
        return {
            'TESTING': cls.TESTING,
            'WTF_CSRF_ENABLED': cls.WTF_CSRF_ENABLED,
            'LOGIN_DISABLED': cls.LOGIN_DISABLED,
        }
    
    @classmethod
    def setup_test_environment(cls):
        """Setup test environment with mocks."""
        # Mock external API calls
        if cls.MOCK_YFINANCE:
            cls.mock_yfinance()
        
        # Mock file system operations that might conflict
        cls.mock_file_operations()
    
    @classmethod
    def mock_yfinance(cls):
        """Mock yfinance API calls."""
        from unittest.mock import patch, MagicMock
        
        # This will be applied in individual tests as needed
        pass
    
    @classmethod
    def mock_file_operations(cls):
        """Mock file operations that might conflict with running app."""
        from unittest.mock import patch
        
        # This will be applied in individual tests as needed
        pass

def create_test_database():
    """Create a test database for isolated testing."""
    # This would create a separate test database
    # Implementation depends on your database setup
    pass

def cleanup_test_database():
    """Clean up test database after tests."""
    # This would clean up the test database
    # Implementation depends on your database setup
    pass
