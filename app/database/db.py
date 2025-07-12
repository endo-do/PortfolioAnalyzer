"""Handles interactions between the front- and backend"""

from app.database.connection import get_db_connection, db_cursor

def fetch_one(query, args=None, dictionary=False):
    args = args or ()
    with db_cursor(dictionary=dictionary) as cursor:
        cursor.execute(query, args)
        return cursor.fetchone()

def fetch_all(query, args=None, dictionary=False):
    args = args or ()
    with db_cursor(dictionary=dictionary) as cursor:
        cursor.execute(query, args)
        return cursor.fetchall()


def execute_change_query(query, args=None):
    args = args or ()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def call_procedure(proc_name, args=None, dictionary=False):
    args = args or ()
    with db_cursor(dictionary=dictionary) as cursor:
        cursor.callproc(proc_name, args)
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return results