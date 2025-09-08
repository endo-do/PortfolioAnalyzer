import os
import glob
from config import DB_CONFIG
from app.database.connection.pool import get_db_connection
from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.status.initiate_status_table import insert_initial_update_status
from app.database.tables.sector.insert_sectors import insert_sectors
from app.database.tables.user.create_default_admin_user import create_default_admin_user
from app.database.tables.currency.insert_default_currencies import insert_default_currencies
from app.database.tables.bondcategory.insert_default_bondcategories import insert_default_bondcategories
from app.database.tables.exchange.insert_exchange import insert_exchanges
from app.database.tables.region.insert_region import insert_regions
from app.database.tables.bond.insert_security_testdata import insert_test_stocks
from app.database.tables.portfolio.insert_portfolios_for_admin import insert_portfolios_for_admin

# Constants
MYSQL_DB = 'portfolioanalyzer'
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tables'))
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs'))

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
            print(f"    ⚠️ Could not create logs directory: {e}")
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
                print(f"    🗑️ Removed: {os.path.basename(log_file)}")
                cleared_count += 1
            except PermissionError:
                print(f"    🔒 Skipped (in use): {os.path.basename(log_file)}")
                locked_files += 1
            except Exception as e:
                print(f"    ⚠️ Could not remove {os.path.basename(log_file)}: {e}")
    
    if cleared_count == 0 and locked_files == 0:
        print("    ℹ️ No log files found to clear")
    elif cleared_count > 0 and locked_files > 0:
        print(f"    ✅ Cleared {cleared_count} log file(s), {locked_files} file(s) in use")
    elif cleared_count > 0:
        print(f"    ✅ Cleared {cleared_count} log file(s)")
    elif locked_files > 0:
        print(f"    ℹ️ {locked_files} log file(s) in use (application running)")

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
        print(f"    ✅ Executed: {path}")
    except Exception as e:
        print(f"    ❌ Error executing {path}: {e}")
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
    # Clear logs before starting database setup
    clear_logs()
    
    print("🧨 Dropping and recreating database...")
    execute_change_query("DROP DATABASE IF EXISTS portfolioanalyzer")
    execute_change_query("CREATE DATABASE portfolioanalyzer")

    # Map: table_name -> dict with booleans for data/testdata presence
    entity_order = {
        "user":           {"data": True,  "testdata": False},
        "sector":         {"data": True,  "testdata": False},
        "region":         {"data": True,  "testdata": False},
        "currency":       {"data": True,  "testdata": False},
        "exchangerate":   {"data": False, "testdata": False},
        "bondcategory":   {"data": True,  "testdata": False},
        "exchange":       {"data": False, "testdata": True},
        "bond":           {"data": False, "testdata": True},
        "bonddata":       {"data": False, "testdata": False},
        "portfolio":      {"data": False, "testdata": True},
        "portfolio_bond": {"data": False, "testdata": True},
        "status":  {"data": True,  "testdata": False},
    }

    all_sql_files = get_sql_files()
    executed_files = set()

    # Step 1: Run all CREATE scripts in order
    print("🚀 Running CREATE scripts...")
    for name in entity_order.keys():
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
            print(f"⚠️ CREATE file not found: {expected_file}")

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

    print("👤 Creating default admin user...")
    create_default_admin_user()

    print("🏷️ Inserting bond categories...")
    insert_default_bondcategories()

    print("💱 Inserting default currencies...")
    insert_default_currencies()

    print("📈 Inserting default exchanges...")
    insert_exchanges()

    print("📈 Inserting default stocks...")
    insert_test_stocks(["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX", "VTI", "SPY", "IEMG",
                        "IEF", "VFIAX", "NESN.SW", "SAP.DE", "7203.T", "0700.HK", "AIR.DE", "BMW.DE",])

    print("🗂️ Creating portfolios for admin...")
    insert_portfolios_for_admin()
    
    print("✅ Marking system as generated.")
    execute_change_query("UPDATE status SET system_generated = NOW()")
    print("🎉 System generation complete.")

if __name__ == '__main__':
    main()
