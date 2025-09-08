"""
Test-specific configuration for Portfolio Analyzer tests.
"""

import os
import tempfile
from unittest.mock import patch

class TestConfig:
    """Configuration for test environment."""
    
    # Test database configuration
    TEST_DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',  # Adjust as needed
        'password': '',  # Adjust as needed
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
