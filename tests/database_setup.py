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

def create_test_database(verbose=False):
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
        if verbose:
            print(f"✅ Test database '{test_config['database']}' created/verified")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating test database: {e}")
        return False

def drop_test_database(verbose=False):
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
        if verbose:
            print(f"🗑️ Test database '{test_config['database']}' dropped")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ Error dropping test database: {e}")
        return False

def setup_test_database(verbose=False):
    """Set up the test database with lightweight data for testing."""
    from app.database.setup.setup import create_database, test_database_connection, get_sql_files, execute_sql_file
    from app.database.helpers.execute_change_query import execute_change_query
    
    test_config = get_test_db_config()
    
    # Always drop and recreate the test database for clean testing
    if verbose:
        print("🗑️ Dropping existing test database...")
    drop_test_database(verbose=verbose)
    
    if verbose:
        print("🔧 Creating fresh test database...")
    create_test_database(verbose=verbose)
    
    # Temporarily override the database config
    import config
    original_config = config.DB_CONFIG.copy()
    config.DB_CONFIG.update(test_config)
    
    # Also override the connection pool to use test database
    from app.database.connection import pool
    original_pool = pool.connection_pool
    pool.connection_pool = None  # Force reinitialization
    
    try:
        # Create database and test connection
        create_database()
        if not test_database_connection():
            print("❌ Cannot proceed with test setup - database connection failed")
            return False
        
        # Create all tables (same as production)
        entity_order = [
            "sector", 
            "region",
            "currency",
            "user",
            "exchangerate",
            "bondcategory",
            "exchange",
            "bond",
            "bonddata",
            "portfolio",
            "portfolio_bond",
            "api_fetch_logs",
            "status"
        ]

        all_sql_files = get_sql_files()
        executed_files = set()

        # Step 1: Run all CREATE scripts in order
        if verbose:
            print("🚀 Creating test database tables...")
        for name in entity_order:
            found = False
            expected_file = f"create_{name}.sql"
            for f in all_sql_files:
                filename = os.path.basename(f).lower()
                if filename == expected_file:
                    execute_sql_file(f)
                    executed_files.add(f)
                    found = True
                    break
            if not found and verbose:
                print(f"⚠️  CREATE file not found: {expected_file}")

        # Step 2: Run any other remaining SQL files (triggers, procedures, etc.)
        if verbose:
            print("📦 Creating triggers and procedures...")
        for f in sorted(all_sql_files):
            if f not in executed_files:
                execute_sql_file(f)

        # Step 3: Insert MINIMAL test data (no external API calls!)
        if verbose:
            print("🔧 Inserting minimal test data...")
        
        # Insert initial status
        from app.database.tables.status.initiate_status_table import insert_initial_update_status
        insert_initial_update_status()
        
        # Insert minimal regions (just a few for testing)
        execute_change_query("""
            INSERT INTO region (region) VALUES 
            ('North America'),
            ('Europe'),
            ('Asia')
        """)
        
        # Insert minimal sectors (just a few for testing)
        execute_change_query("""
            INSERT INTO sector (sectorname, sectordisplayname) VALUES 
            ('Technology', 'Technology'),
            ('Finance', 'Finance'),
            ('Healthcare', 'Healthcare')
        """)
        
        # Insert minimal bond categories (just a few for testing)
        execute_change_query("""
            INSERT INTO bondcategory (bondcategoryname) VALUES 
            ('Government Bonds'),
            ('Corporate Bonds'),
            ('Municipal Bonds')
        """)
        
        # Insert minimal currencies (just USD and EUR for testing)
        execute_change_query("""
            INSERT INTO currency (currencycode, currencyname) VALUES 
            ('USD', 'US Dollar'),
            ('EUR', 'Euro')
        """)
        
        # Create admin user
        from app.database.tables.user.create_default_admin_user import create_default_admin_user
        create_default_admin_user()
        
        # Insert minimal exchanges (just a couple for testing)
        execute_change_query("""
            INSERT INTO exchange (exchangename, region) VALUES 
            ('NYSE', 1),
            ('NASDAQ', 1)
        """)
        
        # Insert minimal bonds/securities (just a few for testing)
        execute_change_query("""
            INSERT INTO bond (bondname, bondsymbol, bondcategoryid, bondcurrencyid, bondsectorid, bondexchangeid) VALUES 
            ('Apple Inc', 'AAPL', 2, 1, 1, 1),
            ('Microsoft Corp', 'MSFT', 2, 1, 1, 1),
            ('Tesla Inc', 'TSLA', 2, 1, 1, 1)
        """)
        
        # Create minimal portfolios for admin
        execute_change_query("""
            INSERT INTO portfolio (portfolioname, portfoliodescription, userid, portfoliocurrencyid) VALUES 
            ('Test Portfolio 1', 'A test portfolio', 1, 1),
            ('Test Portfolio 2', 'Another test portfolio', 1, 2)
        """)
        
        # Mark system as generated
        execute_change_query("UPDATE status SET system_generated = NOW()")
        
        if verbose:
            print(f"✅ Test database '{test_config['database']}' set up successfully with minimal data")
        else:
            print("✅ Test database ready")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up test database: {e}")
        return False
    finally:
        # Restore original config and pool
        config.DB_CONFIG.update(original_config)
        pool.connection_pool = original_pool

def cleanup_test_database(verbose=False):
    """Clean up test database by dropping it."""
    return drop_test_database(verbose=verbose)

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
