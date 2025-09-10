"""
Test database setup and teardown utilities.
"""

import mysql.connector
from mysql.connector import Error
from test_config import get_test_db_config, get_prod_db_config
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_test_database():
    """Create the test database if it doesn't exist."""
    test_config = get_test_db_config()
    prod_config = get_prod_db_config()
    
    # Connect without specifying database
    connection_config = {
        'host': test_config['host'],
        'user': test_config['user'],
        'password': test_config['password']
    }
    
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        
        # Create test database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {test_config['database']}")
        print(f"✅ Test database '{test_config['database']}' created/verified")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating test database: {e}")
        return False

def drop_test_database():
    """Drop the test database."""
    test_config = get_test_db_config()
    
    # Connect without specifying database
    connection_config = {
        'host': test_config['host'],
        'user': test_config['user'],
        'password': test_config['password']
    }
    
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        
        # Drop test database
        cursor.execute(f"DROP DATABASE IF EXISTS {test_config['database']}")
        print(f"🗑️ Test database '{test_config['database']}' dropped")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error dropping test database: {e}")
        return False

def setup_test_database():
    """Set up the test database with all tables and initial data."""
    from app.database.setup.setup import main as setup_database
    
    test_config = get_test_db_config()
    
    # Temporarily override the database config
    import config
    original_config = config.DB_CONFIG.copy()
    config.DB_CONFIG.update(test_config)
    
    # Also override the connection pool to use test database
    from app.database.connection import pool
    original_pool = pool.connection_pool
    pool.connection_pool = None  # Force reinitialization
    
    try:
        # Set up the database
        setup_database()
        print(f"✅ Test database '{test_config['database']}' set up successfully")
        return True
    except Exception as e:
        print(f"❌ Error setting up test database: {e}")
        return False
    finally:
        # Restore original config and pool
        config.DB_CONFIG.update(original_config)
        pool.connection_pool = original_pool

def cleanup_test_database():
    """Clean up test database by dropping it."""
    return drop_test_database()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test database management')
    parser.add_argument('action', choices=['create', 'drop', 'setup', 'cleanup'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_test_database()
    elif args.action == 'drop':
        drop_test_database()
    elif args.action == 'setup':
        create_test_database()
        setup_test_database()
    elif args.action == 'cleanup':
        cleanup_test_database()
