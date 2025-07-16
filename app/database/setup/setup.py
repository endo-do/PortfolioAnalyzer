import os
from config import DB_CONFIG
from app.database.connection.pool import get_db_connection
from app.database.helpers.execute_change_query import execute_change_query

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
        "portfolio_guest":{"data": False, "testdata": False},
        "update_status":  {"data": True,  "testdata": False},
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

    # Step 2: Run DATA scripts if configured
    print("🧪 Running DATA scripts...")
    for name, flags in entity_order.items():
        if not flags.get("data", False):
            continue
        found = False
        expected_file = f"{name}_data.sql"
        for f in all_sql_files:
            filename = os.path.basename(f).lower()
            if filename == expected_file and f not in executed_files:
                execute_sql_file(f)
                executed_files.add(f)
                found = True
                break
        if not found:
            print(f"⚠️ DATA file not found: {expected_file}")

    # Step 3: Run TESTDATA scripts if configured
    print("🧪 Running TEST DATA scripts...")
    for name, flags in entity_order.items():
        if not flags.get("testdata", False):
            continue
        found = False
        expected_file = f"{name}_testdata.sql"
        for f in all_sql_files:
            filename = os.path.basename(f).lower()
            if filename == expected_file and f not in executed_files:
                execute_sql_file(f)
                executed_files.add(f)
                found = True
                break
        if not found:
            print(f"⚠️ TEST DATA file not found: {expected_file}")

    # Step 4: Run any other remaining SQL files not executed yet
    print("📦 Running remaining SQL files such as triggers, procedures, etc...")
    for f in sorted(all_sql_files):
        if f not in executed_files:
            execute_sql_file(f)


if __name__ == '__main__':
    main()
