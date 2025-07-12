from contextlib import contextmanager
from .pool import get_db_connection

@contextmanager
def db_cursor(dictionary=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
    finally:
        cursor.close()
        try:
            conn.close()
        except:
            pass 