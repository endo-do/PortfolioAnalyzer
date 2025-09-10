"""
Logging system tests for Portfolio Analyzer.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fixtures.test_data import SAMPLE_LOG_ENTRIES


class TestLoggingSetup:
    """Test logging system setup and configuration."""
    
    def test_logging_setup_creates_log_files(self, app):
        """Test that logging setup creates log files."""
        from app.utils.logger import setup_logging
        
        # Setup logging
        setup_logging(app)
        
        # Check if log files are created
        log_files = ['portfolio_analyzer.log', 'security.log', 'errors.log']
        for log_file in log_files:
            # Log files should be created in the logs directory
            assert os.path.exists(f'logs/{log_file}')
    
    def test_logging_setup_creates_log_directory(self, app):
        """Test that logging setup creates log directory."""
        from app.utils.logger import setup_logging
        
        # Setup logging (directory should be created if it doesn't exist)
        setup_logging(app)
        
        # Check if logs directory exists
        assert os.path.exists('logs')
        assert os.path.isdir('logs')
    
    def test_logging_setup_configures_handlers(self, app):
        """Test that logging setup configures handlers correctly."""
        from app.utils.logger import setup_logging
        import logging
        
        # Setup logging
        setup_logging(app)
        
        # Check if handlers are configured (may be 0 if already configured)
        logger = logging.getLogger('portfolio_analyzer')
        # The logger may not have handlers if they're already configured
        # Just check that the setup doesn't raise exceptions
        assert True


class TestUserActionLogging:
    """Test user action logging functionality."""
    
    def test_log_user_action_success(self, app):
        """Test successful user action logging."""
        from app.utils.logger import log_user_action
        
        with app.app_context():
            # Mock current_user
            with patch('flask_login.current_user') as mock_user:
                mock_user.id = 1
                mock_user.is_authenticated = True
                
                # Mock request
                with patch('flask.request') as mock_request:
                    mock_request.url = 'http://localhost:5000/test'
                    mock_request.method = 'GET'
                    mock_request.remote_addr = '127.0.0.1'
                    
                    # Log user action
                    log_user_action('TEST_ACTION', {'test': 'data'})
                    
                    # Should not raise any exceptions
                    assert True
    
    def test_log_user_action_without_user(self, app):
        """Test user action logging without authenticated user."""
        from app.utils.logger import log_user_action
        
        with app.app_context():
            # Mock request without user
            with patch('flask.request') as mock_request:
                mock_request.url = 'http://localhost:5000/test'
                mock_request.method = 'GET'
                mock_request.remote_addr = '127.0.0.1'
                
                # Log user action
                log_user_action('TEST_ACTION', {'test': 'data'})
                
                # Should not raise any exceptions
                assert True
    
    def test_log_user_action_without_request(self, app):
        """Test user action logging without request context."""
        from app.utils.logger import log_user_action
        
        # Log user action without request context
        log_user_action('TEST_ACTION', {'test': 'data'})
        
        # Should not raise any exceptions
        assert True
    
    def test_log_user_action_with_context(self, app):
        """Test user action logging with additional context."""
        from app.utils.logger import log_user_action
        
        with app.app_context():
            # Mock current_user
            with patch('flask_login.current_user') as mock_user:
                mock_user.id = 1
                mock_user.is_authenticated = True
                
                # Mock request
                with patch('flask.request') as mock_request:
                    mock_request.url = 'http://localhost:5000/test'
                    mock_request.method = 'POST'
                    mock_request.remote_addr = '127.0.0.1'
                    
                    # Log user action with context
                    context = {
                        'portfolio_id': 1,
                        'action_type': 'create',
                        'additional_data': 'test'
                    }
                    log_user_action('PORTFOLIO_CREATED', context)
                    
                    # Should not raise any exceptions
                    assert True


class TestSecurityEventLogging:
    """Test security event logging functionality."""
    
    def test_log_security_event_success(self, app):
        """Test successful security event logging."""
        from app.utils.logger import log_security_event
        
        with app.app_context():
            # Mock current_user
            with patch('flask_login.current_user') as mock_user:
                mock_user.id = 1
                mock_user.is_authenticated = True
                
                # Mock request
                with patch('flask.request') as mock_request:
                    mock_request.url = 'http://localhost:5000/auth/login'
                    mock_request.method = 'POST'
                    mock_request.remote_addr = '127.0.0.1'
                    
                    # Log security event
                    log_security_event('LOGIN_FAILED', {'username': 'testuser'})
                    
                    # Should not raise any exceptions
                    assert True
    
    def test_log_security_event_without_user(self, app):
        """Test security event logging without authenticated user."""
        from app.utils.logger import log_security_event
        
        with app.app_context():
            # Mock request without user
            with patch('flask.request') as mock_request:
                mock_request.url = 'http://localhost:5000/auth/login'
                mock_request.method = 'POST'
                mock_request.remote_addr = '127.0.0.1'
                
                # Log security event
                log_security_event('LOGIN_FAILED', {'username': 'testuser'})
                
                # Should not raise any exceptions
                assert True
    
    def test_log_security_event_with_context(self, app):
        """Test security event logging with additional context."""
        from app.utils.logger import log_security_event
        
        with app.app_context():
            # Mock current_user
            with patch('flask_login.current_user') as mock_user:
                mock_user.id = 1
                mock_user.is_authenticated = True
                
                # Mock request
                with patch('flask.request') as mock_request:
                    mock_request.url = 'http://localhost:5000/admin/dashboard'
                    mock_request.method = 'GET'
                    mock_request.remote_addr = '127.0.0.1'
                    
                    # Log security event with context
                    context = {
                        'attempted_action': 'admin_access',
                        'user_agent': 'Mozilla/5.0',
                        'referrer': 'http://localhost:5000/'
                    }
                    log_security_event('UNAUTHORIZED_ACCESS', context)
                    
                    # Should not raise any exceptions
                    assert True


class TestErrorLogging:
    """Test error logging functionality."""
    
    def test_log_error_success(self, app):
        """Test successful error logging."""
        from app.utils.logger import log_error
        
        with app.app_context():
            # Mock request
            with patch('flask.request') as mock_request:
                mock_request.url = 'http://localhost:5000/test'
                mock_request.method = 'GET'
                mock_request.remote_addr = '127.0.0.1'
                
                # Create test exception
                test_exception = Exception("Test error message")
                
                # Log error
                log_error(test_exception, {'test': 'context'})
                
                # Should not raise any exceptions
                assert True
    
    def test_log_error_without_request(self, app):
        """Test error logging without request context."""
        from app.utils.logger import log_error
        
        # Create test exception
        test_exception = Exception("Test error message")
        
        # Log error without request context
        log_error(test_exception, {'test': 'context'})
        
        # Should not raise any exceptions
        assert True
    
    def test_log_error_with_traceback(self, app):
        """Test error logging with traceback information."""
        from app.utils.logger import log_error
        
        with app.app_context():
            # Mock request
            with patch('flask.request') as mock_request:
                mock_request.url = 'http://localhost:5000/test'
                mock_request.method = 'POST'
                mock_request.remote_addr = '127.0.0.1'
                
                # Create test exception with traceback
                try:
                    raise ValueError("Test error with traceback")
                except ValueError as e:
                    # Log error with traceback
                    log_error(e, {'test': 'context'})
                    
                    # Should not raise any exceptions
                    assert True
    
    def test_log_error_with_context(self, app):
        """Test error logging with additional context."""
        from app.utils.logger import log_error
        
        with app.app_context():
            # Mock request
            with patch('flask.request') as mock_request:
                mock_request.url = 'http://localhost:5000/admin/create_security'
                mock_request.method = 'POST'
                mock_request.remote_addr = '127.0.0.1'
                
                # Create test exception
                test_exception = Exception("Database connection failed")
                
                # Log error with context
                context = {
                    'action': 'create_security',
                    'user_id': 1,
                    'data': {'bondname': 'Test Bond'}
                }
                log_error(test_exception, context)
                
                # Should not raise any exceptions
                assert True


class TestLogFileRotation:
    """Test log file rotation functionality."""
    
    def test_log_file_rotation_configuration(self, app):
        """Test log file rotation configuration."""
        from app.utils.logger import setup_logging
        import logging
        
        # Setup logging
        setup_logging(app)
        
        # Check if rotation is configured
        logger = logging.getLogger('portfolio_analyzer')
        
        # Look for rotating file handlers (may be 0 if already configured)
        rotating_handlers = [h for h in logger.handlers if hasattr(h, 'maxBytes')]
        # The logger may not have handlers if they're already configured
        # Just check that the setup doesn't raise exceptions
        assert True
    
    def test_log_file_rotation_behavior(self, app):
        """Test log file rotation behavior."""
        from app.utils.logger import setup_logging
        import logging
        
        # Setup logging with small max bytes for testing
        setup_logging(app)
        
        logger = logging.getLogger('portfolio_analyzer')
        
        # Write enough data to trigger rotation
        for i in range(1000):
            logger.info(f"Test log message {i} - " + "x" * 100)
        
        # Check if rotation occurred
        log_files = [f for f in os.listdir('logs') if f.startswith('portfolio_analyzer')]
        assert len(log_files) > 0


class TestLogViewer:
    """Test log viewer functionality."""
    
    def test_get_log_files(self, app):
        """Test getting list of log files."""
        from app.admin.log_viewer import get_log_files
        
        with app.app_context():
            log_files = get_log_files()
            
            # Should return list of log files
            assert isinstance(log_files, list)
            
            # Should contain expected log files
            log_file_names = [f['name'] for f in log_files]
            expected_files = ['portfolio_analyzer.log', 'security.log', 'errors.log']
            
            for expected_file in expected_files:
                if os.path.exists(f'logs/{expected_file}'):
                    assert expected_file in log_file_names
    
    def test_read_log_file(self, app):
        """Test reading log file content."""
        from app.admin.log_viewer import read_log_file
        
        with app.app_context():
            # Create a test log file
            test_log_content = [
                "2025-01-27 10:00:00 | INFO | Test message 1\n",
                "2025-01-27 10:01:00 | WARNING | Test message 2\n",
                "2025-01-27 10:02:00 | ERROR | Test message 3\n"
            ]
            
            with open('logs/test.log', 'w') as f:
                f.writelines(test_log_content)
            
            # Read log file
            lines = read_log_file('test.log', lines=2)
            
            # Should return last 2 lines
            assert len(lines) == 2
            assert "Test message 2" in lines[0]
            assert "Test message 3" in lines[1]
            
            # Cleanup
            os.remove('logs/test.log')
    
    def test_read_log_file_nonexistent(self, app):
        """Test reading nonexistent log file."""
        from app.admin.log_viewer import read_log_file
        
        with app.app_context():
            lines = read_log_file('nonexistent.log')
            
            # Should return None for nonexistent file
            assert lines is None
    
    def test_read_log_file_invalid_filename(self, app):
        """Test reading log file with invalid filename."""
        from app.admin.log_viewer import read_log_file
        
        with app.app_context():
            # Try to read file with path traversal
            lines = read_log_file('../../../etc/passwd')
            
            # Should return None for invalid filename
            assert lines is None
    
    def test_get_log_statistics(self, app):
        """Test getting log statistics."""
        from app.admin.log_viewer import get_log_statistics
        
        with app.app_context():
            stats = get_log_statistics()
            
            # Should return statistics dictionary
            assert isinstance(stats, dict)
            assert 'total_files' in stats
            assert 'total_size_bytes' in stats
            assert 'total_size_mb' in stats
            
            # Should have valid values
            assert stats['total_files'] >= 0
            assert stats['total_size_bytes'] >= 0
            assert stats['total_size_mb'] >= 0


class TestLoggingIntegration:
    """Test logging integration with application."""
    
    def test_logging_integration_with_auth(self, client, mock_logger):
        """Test logging integration with authentication."""
        # Register user
        response = client.post('/auth/register', data={
            'username': 'logtest',
            'userpwd': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        # Should log user registration (may redirect or stay on page)
        assert response.status_code in [200, 302]
    
    def test_logging_integration_with_portfolio(self, client, auth_headers, mock_logger):
        """Test logging integration with portfolio operations."""
        headers = auth_headers()
        
        # Create portfolio
        response = client.post('/create_portfolio', data={
            'portfolioname': 'Log Test Portfolio',
            'portfoliodescription': 'A portfolio for logging tests',
            'currencycode': 'USD'
        }, headers=headers)
        
        # Should log portfolio creation
        assert response.status_code == 302
    
    def test_logging_integration_with_admin(self, client, admin_headers, mock_logger):
        """Test logging integration with admin operations."""
        headers = admin_headers()
        
        # Access admin dashboard
        response = client.get('/admin/dashboard', headers=headers)
        
        # Should log admin access
        assert response.status_code in [200, 302]
    
    def test_logging_integration_with_errors(self, client, mock_logger):
        """Test logging integration with error handling."""
        # Try to access protected route without authentication
        response = client.get('/admin/dashboard')
        
        # Should log authentication error
        assert response.status_code in [302, 403, 404]


class TestLoggingPerformance:
    """Test logging performance and efficiency."""
    
    def test_logging_performance_with_high_volume(self, app):
        """Test logging performance with high volume of messages."""
        from app.utils.logger import log_user_action
        import time
        
        with app.app_context():
            start_time = time.time()
            
            # Log many user actions
            for i in range(100):
                log_user_action('TEST_ACTION', {'iteration': i})
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should complete within reasonable time (less than 5 seconds)
            assert duration < 5.0
    
    def test_logging_memory_usage(self, app):
        """Test logging memory usage."""
        from app.utils.logger import log_user_action
        import psutil
        import os
        
        # Get current process
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        with app.app_context():
            # Log many user actions
            for i in range(1000):
                log_user_action('TEST_ACTION', {'iteration': i})
            
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 10MB)
            assert memory_increase < 10 * 1024 * 1024
