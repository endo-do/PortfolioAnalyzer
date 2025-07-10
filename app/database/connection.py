from contextlib import contextmanager
from mysql.connector import pooling
from flask_login import UserMixin
from config import DB_CONFIG


class User(UserMixin):
    def __init__(self, id, username, password, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

connection_pool = None

def init_db_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name='mypool',
            pool_size=5,
            **DB_CONFIG
        )

def get_db_connection():
    if connection_pool is None:
        init_db_pool()
    return connection_pool.get_connection()

@contextmanager
def db_cursor(dictionary=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        # kein commit, da nur für SELECT gedacht
    finally:
        cursor.close()
        try:
            conn.close()
        except:
            pass 