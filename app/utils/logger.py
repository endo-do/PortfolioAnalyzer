# Logging system for Portfolio Analyzer - provides structured logging with file rotation, security events, and error tracking
"""
Logging configuration for Portfolio Analyzer application.
Provides structured logging with file rotation and console output.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from flask import request
from functools import wraps
from config import LOG_MAX_BYTES, LOG_BACKUP_COUNT, SECURITY_LOG_MAX_BYTES, SECURITY_LOG_BACKUP_COUNT, ERROR_LOG_MAX_BYTES, ERROR_LOG_BACKUP_COUNT

def setup_logging(app):
    """
    Configure logging for the Flask application.
    
    Logs are saved to:
    - logs/portfolio_analyzer.log (main application log)
    - logs/security.log (security-related events)
    - logs/errors.log (error logs only)
    - Console output (for development)
    """
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    app.logger.setLevel(logging.INFO)
    
    # Remove default handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. Main application log (rotating file)
    main_log_file = os.path.join(log_dir, 'portfolio_analyzer.log')
    main_handler = logging.handlers.RotatingFileHandler(
        main_log_file, 
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    main_handler.setLevel(logging.INFO)
    main_handler.setFormatter(detailed_formatter)
    app.logger.addHandler(main_handler)
    
    # 2. Security log (separate file for security events)
    security_log_file = os.path.join(log_dir, 'security.log')
    security_handler = logging.handlers.RotatingFileHandler(
        security_log_file,
        maxBytes=SECURITY_LOG_MAX_BYTES,
        backupCount=SECURITY_LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.setFormatter(detailed_formatter)
    
    # Create security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.WARNING)
    security_logger.addHandler(security_handler)
    security_logger.propagate = False  # Don't propagate to root logger
    
    # 3. Error log (errors only)
    error_log_file = os.path.join(log_dir, 'errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=ERROR_LOG_MAX_BYTES,
        backupCount=ERROR_LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Create error logger
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)
    error_logger.addHandler(error_handler)
    error_logger.propagate = False
    
    # 4. Console handler (for development)
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(simple_formatter)
        app.logger.addHandler(console_handler)
    
    # Log application startup
    app.logger.info("=" * 60)
    app.logger.info("Portfolio Analyzer Application Started")
    app.logger.info(f"Log files: {log_dir}")
    app.logger.info("=" * 60)

def log_user_action(action, details=None, user_id=None):
    """
    Log user actions with context.
    
    Args:
        action (str): Description of the action
        details (dict): Additional details about the action
        user_id (int): User ID (if not provided, tries to get from current_user)
    """
    try:
        if user_id is None:
            try:
                from flask_login import current_user
                if hasattr(current_user, 'id'):
                    user_id = current_user.id
            except ImportError:
                pass
        
        log_data = {
            'action': action,
            'user_id': user_id,
            'ip_address': request.remote_addr if request else 'N/A',
            'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            log_data['details'] = details
        
        if current_app and hasattr(current_app, 'logger'):
            current_app.logger.info(f"USER_ACTION: {action} | User: {user_id} | IP: {log_data['ip_address']} | Details: {details}")
        else:
            print(f"USER_ACTION: {action} | User: {user_id} | Details: {details}")
        
    except Exception as e:
        # Fallback logging if there's an issue with the main logging
        print(f"Logging error: {e}")

def log_security_event(event_type, message, user_id=None, severity='WARNING'):
    """
    Log security-related events.
    
    Args:
        event_type (str): Type of security event (LOGIN_FAILED, UNAUTHORIZED_ACCESS, etc.)
        message (str): Description of the event
        user_id (int): User ID if applicable
        severity (str): Log level (WARNING, ERROR, CRITICAL)
    """
    try:
        security_logger = logging.getLogger('security')
        
        log_data = {
            'event_type': event_type,
            'message': message,
            'user_id': user_id,
            'ip_address': request.remote_addr if request else 'N/A',
            'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
            'timestamp': datetime.now().isoformat()
        }
        
        log_message = f"SECURITY: {event_type} | {message} | User: {user_id} | IP: {log_data['ip_address']}"
        
        if severity == 'ERROR':
            security_logger.error(log_message)
        elif severity == 'CRITICAL':
            security_logger.critical(log_message)
        else:
            security_logger.warning(log_message)
            
    except Exception as e:
        print(f"Security logging error: {e}")

def log_error(error, context=None):
    """
    Log errors with context.
    
    Args:
        error (Exception): The error that occurred
        context (dict): Additional context about where the error occurred
    """
    try:
        error_logger = logging.getLogger('errors')
        
        log_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'ip_address': request.remote_addr if request else 'N/A',
            'timestamp': datetime.now().isoformat()
        }
        
        log_message = f"ERROR: {type(error).__name__} | {str(error)} | Context: {context}"
        error_logger.error(log_message, exc_info=True)
        
    except Exception as e:
        print(f"Error logging failed: {e}")

def log_function_call(func):
    """
    Decorator to log function calls with parameters and execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        
        try:
            # Log function entry
            if current_app and hasattr(current_app, 'logger'):
                current_app.logger.debug(f"FUNCTION_CALL: {func.__name__} | Args: {args} | Kwargs: {kwargs}")
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Log function exit
            execution_time = (datetime.now() - start_time).total_seconds()
            if current_app and hasattr(current_app, 'logger'):
                current_app.logger.debug(f"FUNCTION_EXIT: {func.__name__} | Execution time: {execution_time:.3f}s")
            
            return result
            
        except Exception as e:
            # Log function error
            execution_time = (datetime.now() - start_time).total_seconds()
            if current_app and hasattr(current_app, 'logger'):
                current_app.logger.error(f"FUNCTION_ERROR: {func.__name__} | Error: {str(e)} | Execution time: {execution_time:.3f}s")
            raise
            
    return wrapper

# Import current_app here to avoid circular imports
try:
    from flask import current_app
except ImportError:
    # Handle case when not in Flask context
    current_app = None
