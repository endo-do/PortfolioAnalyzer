"""
Test-specific database connection handling.
"""

import mysql.connector
from mysql.connector import pooling
from test_config import get_test_db_config

# Test-specific connection pool
test_connection_pool = None

def init_test_db_pool():
    """Initialize test database connection pool."""
    global test_connection_pool
    if test_connection_pool is None:
        test_config = get_test_db_config()
        test_connection_pool = pooling.MySQLConnectionPool(
            pool_name='testpool',
            pool_size=3,  # Smaller pool for tests
            **test_config
        )

def get_test_db_connection():
    """Get a connection from the test database pool."""
    if test_connection_pool is None:
        init_test_db_pool()
    return test_connection_pool.get_connection()

def close_test_db_pool():
    """Close the test database connection pool."""
    global test_connection_pool
    if test_connection_pool:
        # Close all connections in the pool
        try:
            for _ in range(test_connection_pool.pool_size):
                conn = test_connection_pool.get_connection()
                conn.close()
        except:
            pass  # Pool might already be closed
        test_connection_pool = None
