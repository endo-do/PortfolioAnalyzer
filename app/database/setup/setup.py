import os
from config import DB_CONFIG
from app.database.connection.pool import get_db_connection
from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.execute_change_query import execute_change_query
from app.database.tables.status.initiate_status_table import insert_initial_update_status
from app.database.tables.user.create_default_admin_user import create_default_admin_user
from app.database.tables.currency.insert_default_currencies import insert_default_currencies
from app.database.tables.bondcategory.insert_default_bondcategories import insert_default_bondcategories
from app.database.tables.bond.insert_security_testdata import insert_test_stocks
from app.database.tables.portfolio.insert_portfolios_for_admin import insert_portfolios_for_admin

# Constants
MYSQL_DB = 'portfolioanalyzer'
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tables'))

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
        print(f"✅ Executed: {path}")
    except Exception as e:
        print(f"❌ Error executing {path}: {e}")
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
    print("🧨 Dropping and recreating database...")
    execute_change_query("DROP DATABASE IF EXISTS portfolioanalyzer")
    execute_change_query("CREATE DATABASE portfolioanalyzer")

    # Map: table_name -> dict with booleans for data/testdata presence
    entity_order = {
        "user":           {"data": True,  "testdata": False},
        "currency":       {"data": True,  "testdata": False},
        "exchangerate":   {"data": False, "testdata": False},
        "bondcategory":   {"data": True,  "testdata": False},
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

    print("👤 Creating default admin user...")
    create_default_admin_user()

    print("💱 Inserting default currencies...")
    insert_default_currencies()

    print("🏷️ Inserting default bond categories...")
    insert_default_bondcategories()

    print("📈 Inserting test stocks...")
    insert_test_stocks(["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX", "VTI", "SPY", "IEMG"])

    print("🗂️ Creating portfolios for admin...")
    insert_portfolios_for_admin()
    
    print("✅ Marking system as generated.")
    execute_change_query("UPDATE status SET system_generated = NOW()")
    print("🎉 System generation complete.")

if __name__ == '__main__':
    main()
