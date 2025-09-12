from app.database.helpers.execute_change_query import execute_change_query
from datetime import datetime, timezone

def log_api_fetch(symbol, fetch_type, status, error_message=None):
    """
    Log an API fetch attempt to the database.
    
    Args:
        symbol (str): The symbol being fetched (e.g., 'AAPL', 'USDCHF')
        fetch_type (str): Type of fetch ('STOCK' or 'EXCHANGE')
        status (str): Status of the fetch ('SUCCESS', 'FAILED', 'PENDING')
        error_message (str, optional): Error message if the fetch failed
    """
    try:
        query = """
            INSERT INTO api_fetch_logs (symbol, fetch_type, status, error_message, fetch_time)
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_change_query(query, (symbol, fetch_type, status, error_message, datetime.now(timezone.utc)))
    except Exception as e:
        # Don't let logging errors break the main functionality
        print(f"Failed to log API fetch: {e}")

def log_api_fetch_success(symbol, fetch_type):
    """Log a successful API fetch."""
    log_api_fetch(symbol, fetch_type, 'SUCCESS')

def log_api_fetch_failure(symbol, fetch_type, error_message):
    """Log a failed API fetch."""
    log_api_fetch(symbol, fetch_type, 'FAILED', error_message)