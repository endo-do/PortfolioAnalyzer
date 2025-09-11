from mysql.connector import pooling
from config import DB_CONFIG, DB_POOL_SIZE, DB_POOL_NAME

connection_pool = None

def init_db_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name=DB_POOL_NAME,
            pool_size=DB_POOL_SIZE,
            **DB_CONFIG
        )

def get_db_connection():
    if connection_pool is None:
        init_db_pool()
    return connection_pool.get_connection()