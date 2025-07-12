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
            # Entweder ignorieren oder result verarbeiten
            # z.B. result.fetchall() wenn SELECT Statements erwartet werden
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

    entity_order = [
        "user",
        "currency",
        "exchangerate",
        "bondcategory",
        "bond",
        "bonddata",
        "portfolio",
        "portfolio_bond",
        "portfolio_guest"
    ]

    all_sql_files = get_sql_files()
    executed_files = set()

    print("🚀 Running CREATE scripts...")
    for name in entity_order:
        found = False
        for f in all_sql_files:
            filename = os.path.basename(f).lower()
            if filename == f"create_{name}.sql":
                execute_sql_file(f)
                executed_files.add(f)
                found = True
                break
        if not found:
            print(f"⚠️ CREATE file not found: create_{name}.sql")

    # Step 2: run <entity>_test_data.sql in same order (exact match)
    print("🧪 Running TEST DATA scripts...")
    for name in entity_order:
        found = False
        for f in all_sql_files:
            filename = os.path.basename(f).lower()
            if filename == f"{name}_testdata.sql" and f not in executed_files:
                execute_sql_file(f)
                executed_files.add(f)
                found = True
                break
        if not found:
            print(f"⚠️ TEST DATA file not found: {name}_testdata.sql")

    # Step 3: run everything else
    print("📦 Running remaining SQL files...")
    for f in sorted(all_sql_files):
        if f not in executed_files:
            execute_sql_file(f)


if __name__ == '__main__':
    main()
