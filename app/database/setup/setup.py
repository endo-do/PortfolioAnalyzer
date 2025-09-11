import os
import glob
import mysql.connector
from config import DB_CONFIG, DB_ROOT_CONFIG
from app.database.connection.pool import get_db_connection
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.status.initiate_status_table import insert_initial_update_status
from app.database.tables.sector.insert_sectors import insert_sectors
from app.database.tables.user.create_default_admin_user import create_default_admin_user
from app.database.tables.currency.insert_default_currencies import insert_default_currencies
from app.database.tables.bondcategory.insert_default_bondcategories import insert_default_bondcategories
from app.database.tables.exchange.insert_exchange import insert_exchanges
from app.database.tables.region.insert_region import insert_regions
from app.database.tables.bond.insert_default_stocks import insert_default_stocks
from app.database.tables.portfolio.insert_portfolios_for_admin import insert_portfolios_for_admin

# Constants - will be set dynamically
MYSQL_DB = None
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tables'))
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs'))

def database_exists_and_initialized():
    """Check if the database exists and is already initialized."""
    db_name = DB_CONFIG['database']
    
    try:
        # Connect to MySQL server as root
        conn = mysql.connector.connect(
            host=DB_ROOT_CONFIG['host'],
            user=DB_ROOT_CONFIG['user'],
            password=DB_ROOT_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False
        
        # Check if database has tables (indicating it's initialized)
        cursor.execute(f"USE {db_name}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # If we have tables, database is initialized
        return len(tables) > 0
        
    except mysql.connector.Error as e:
        print(f"    ⚠️  Could not check database status: {e}")
        return False
    except Exception as e:
        print(f"    ⚠️  Unexpected error checking database: {e}")
        return False

def create_database():
    """Create the database if it doesn't exist, without requiring a database connection."""
    print("🗄️  Checking database status...")
    
    # Get database name from current config
    db_name = DB_CONFIG['database']
    
    # Validate root database configuration for setup
    if not all([DB_ROOT_CONFIG['host'], DB_ROOT_CONFIG['user'], DB_ROOT_CONFIG['password']]):
        print("    ❌ Root database configuration incomplete. Please check your .env file.")
        print("    Required: DB_HOST, DB_ROOT_USER, DB_ROOT_PASSWORD")
        raise ValueError("Incomplete root database configuration")
    
    # Check if database is already initialized
    if database_exists_and_initialized():
        print(f"    ✅ Database '{db_name}' already exists and is initialized")
        print("    ℹ️  Skipping database creation - using existing database")
        return False  # Return False to indicate no setup needed
    
    # Connect to MySQL server as root (for setup operations)
    try:
        conn = mysql.connector.connect(
            host=DB_ROOT_CONFIG['host'],
            user=DB_ROOT_CONFIG['user'],
            password=DB_ROOT_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Drop database if it exists (only if not initialized)
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"    🗑️  Dropped existing database: {db_name}")
        
        # Create database
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"    ✅ Created database: {db_name}")
        
        cursor.close()
        conn.close()
        return True  # Return True to indicate setup is needed
        
    except mysql.connector.Error as e:
        print(f"    ❌ MySQL Error creating database: {e}")
        print("    💡 Make sure MySQL server is running and credentials are correct")
        raise e
    except Exception as e:
        print(f"    ❌ Unexpected error: {e}")
        raise e

def create_application_user():
    """Create the application user with appropriate privileges."""
    print("👤 Creating application user...")
    
    # Validate application user configuration
    if not all([DB_CONFIG['user'], DB_CONFIG['password']]):
        print("    ❌ Application user configuration incomplete.")
        print("    Required: DB_USER, DB_PASSWORD")
        raise ValueError("Incomplete application user configuration")
    
    try:
        # Connect as root to create the application user
        conn = mysql.connector.connect(
            host=DB_ROOT_CONFIG['host'],
            user=DB_ROOT_CONFIG['user'],
            password=DB_ROOT_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create the application user
        app_user = DB_CONFIG['user']
        app_password = DB_CONFIG['password']
        db_name = DB_CONFIG['database']
        
        # Drop user if exists (for clean setup)
        cursor.execute(f"DROP USER IF EXISTS '{app_user}'@'%'")
        print(f"    🗑️  Dropped existing user: {app_user}")
        
        # Create the application user
        cursor.execute(f"CREATE USER '{app_user}'@'%' IDENTIFIED BY '{app_password}'")
        print(f"    ✅ Created user: {app_user}")
        
        # Grant necessary privileges for application operations
        cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, REFERENCES, TRIGGER ON {db_name}.* TO '{app_user}'@'%'")
        cursor.execute(f"GRANT CREATE ON *.* TO '{app_user}'@'%'")
        
        # Grant additional privileges needed for triggers and procedures
        cursor.execute(f"GRANT SUPER, PROCESS ON *.* TO '{app_user}'@'%'")
        
        # Grant privileges for stored procedures and functions
        cursor.execute(f"GRANT EXECUTE ON {db_name}.* TO '{app_user}'@'%'")
        cursor.execute(f"GRANT CREATE ROUTINE, ALTER ROUTINE ON {db_name}.* TO '{app_user}'@'%'")
        
        cursor.execute("FLUSH PRIVILEGES")
        print(f"    ✅ Granted privileges to: {app_user}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"    ❌ MySQL Error creating application user: {e}")
        raise e
    except Exception as e:
        print(f"    ❌ Unexpected error: {e}")
        raise e

def test_database_connection():
    """Test that we can connect to the newly created database."""
    print("🔍 Testing database connection...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("    ✅ Database connection successful")
        return True
    except Exception as e:
        print(f"    ❌ Database connection failed: {e}")
        return False

def clear_logs():
    """Clear all log files before database setup.
    
    Note: Log files that are currently in use by the application
    (e.g., when Flask is running) cannot be removed and will show
    a warning message. This is expected behavior to prevent data loss.
    """
    print("🧹 Clearing existing log files...")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        try:
            os.makedirs(LOGS_DIR, exist_ok=True)
            print(f"    📁 Created logs directory: {LOGS_DIR}")
        except Exception as e:
            print(f"    ⚠️  Could not create logs directory: {e}")
            return
    
    # Find all log files
    log_patterns = [
        os.path.join(LOGS_DIR, '*.log'),
        os.path.join(LOGS_DIR, '*.log.*'),  # For rotated log files
    ]
    
    cleared_count = 0
    locked_files = 0
    for pattern in log_patterns:
        for log_file in glob.glob(pattern):
            try:
                os.remove(log_file)
                print(f"    🗑️  Removed: {os.path.basename(log_file)}")
                cleared_count += 1
            except PermissionError:
                print(f"    🔒 Skipped (in use): {os.path.basename(log_file)}")
                locked_files += 1
            except Exception as e:
                print(f"    ⚠️  Could not remove {os.path.basename(log_file)}: {e}")
    
    if cleared_count == 0 and locked_files == 0:
        print("    ℹ️  No log files found to clear")
    elif cleared_count > 0 and locked_files > 0:
        print(f"    ✅ Cleared {cleared_count} log file(s), {locked_files} file(s) in use")
    elif cleared_count > 0:
        print(f"    ✅ Cleared {cleared_count} log file(s)")
    elif locked_files > 0:
        print(f"    ℹ️  {locked_files} log file(s) in use (application running)")

def execute_sql_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        sql = f.read()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for result in cursor.execute(sql, multi=True):
            # You can process result.fetchall() if needed
            pass
        conn.commit()
        print(f"    ✅ Executed: {os.path.basename(path)}")
    except Exception as e:
        print(f"    ❌ Error executing {os.path.basename(path)}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_sql_files():
    sql_files = []
    for root, _, files in os.walk(SQL_DIR):
        for file in files:
            if file.endswith('.sql'):
                full_path = os.path.join(root, file)
                sql_files.append(full_path)
    return sql_files

def main():
    print("🚀 Starting database setup...")
    
    # Check if database is already initialized
    if database_exists_and_initialized():
        print("✅ Database is already initialized - skipping setup")
        print("ℹ️  Application is ready to use existing database")
        return
    
    # Clear logs before starting database setup
    clear_logs()
    
    # Create database without requiring existing database connection
    setup_needed = create_database()
    
    if not setup_needed:
        print("✅ Database setup not needed - using existing database")
        return
    
    # Create application user with appropriate privileges
    create_application_user()
    
    # Test that we can connect to the new database with application user
    if not test_database_connection():
        print("❌ Cannot proceed with setup - database connection failed")
        return

    # List of tables in creation order
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
    print("🚀 Running CREATE scripts...")
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
        if not found:
            print(f"⚠️  CREATE file not found: {expected_file}")

    # Step 2: Run any other remaining SQL files not executed yet
    print("📦 Running remaining SQL files such as triggers, procedures, etc...")
    for f in sorted(all_sql_files):
        if f not in executed_files:
            execute_sql_file(f)

    # Step 3: Run INSERT scripts in order

    print("🔧 Starting system generation...")
    insert_initial_update_status()

    print("🌍 Inserting regions...")
    insert_regions()

    print("📊 Inserting sectors...")
    insert_sectors()

    print("🏷️  Inserting bond categories...")
    insert_default_bondcategories()

    print("💱 Inserting default currencies... (might take a while)")
    insert_default_currencies()

    print("👤 Creating default admin user...")
    create_default_admin_user()

    print("📈 Inserting default exchanges...")
    insert_exchanges()

    print("📈 Inserting default stocks... (might take a while)")
    insert_default_stocks()

    print("🗂️  Creating portfolios for admin...")
    insert_portfolios_for_admin()
    
    print("📊 Fetching initial stock prices...")
    from app.database.tables.bond.fetch_daily_securityrates import fetch_daily_securityrates
    fetch_daily_securityrates()
    
    print("💱 Fetching initial exchange rates...")
    from app.database.tables.exchangerate.fetch_daily_exchangerates import fetch_daily_exchangerates
    fetch_daily_exchangerates()
    
    print("✅ Marking system as generated.")
    execute_change_query("UPDATE status SET system_generated = NOW()")
    print("🎉 System generation complete.")
    print("🚀 Database is ready for application startup!")

if __name__ == '__main__':
    main()
