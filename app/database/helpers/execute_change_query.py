from app.database.connection.cursor import get_db_connection


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