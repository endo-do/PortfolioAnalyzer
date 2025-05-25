"""Handles interactions between the front- and backend"""


from mysql.connector import pooling
from flask_login import UserMixin
from config import DB_CONFIG


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

connection_pool = None

def init_db_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **DB_CONFIG
        )

def get_db_connection():
    if connection_pool is None:
        init_db_pool()
    return connection_pool.get_connection()

def release_db_connection(conn):
    conn.close()

def get_user_by_id(user_id):
    """
    get user details from db based on userid

    Args:
        user_id (int): user id

    Returns:
        User: User class, None if no matching user was found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT userid, username, userpwd FROM users WHERE userid = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)

    if result:
        return User(id=result[0], username=result[1], password=result[2])
    return None

def get_all_currency_pairs():
    """
    Returns all distinct pairs of currencies

    Returns:
        list: list of all distinct pairs
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT currencyid FROM currencies")
    currencies = [row[0] for row in cursor.fetchall()]
    pairs = []
    for base in currencies:
        for quote in currencies:
            pairs.append((base, quote))
    cursor.close()
    release_db_connection(conn)
    
    return pairs

def exchange_rate_exists(from_currency_id, to_currency_id, date):
    """
    Check if an exchange rate record exists for given currencies and date

    Args:
        cursor: Database cursor
        from_currency_id (int): currencyid of base currency
        to_currency_id (int): currencyid of quote currency
        date (datetime.date): date to check

    Returns:
        bool: True if record exists, else False
    """
    query = """
        SELECT 1 FROM exchangerates
        WHERE fromcurrencyid = %s AND tocurrencyid = %s AND exchangeratelogtime = %s
        LIMIT 1
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (from_currency_id, to_currency_id, date))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)
    
    return result is not None

def get_currency_code_by_id(currency_id):
    """
    Returns currency code based on its id in the database

    Args:
        currency_id (int): currencyid
    
    Returns:
        str: currency code or None
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT currencycode FROM currencies
        WHERE currencyid = %s
    """, (currency_id,))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)

    return result[0] if result else None

def get_user_portfolios(userid):
    """
    Returns all portfolios of a user with basic informations

    Args:
        userid (int): userid

    Returns:
        list: list of portfolios as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("get_user_portfolios_with_values", (userid,))
    portfolios = []
    
    for result in cursor.stored_results():
        portfolios.extend(result.fetchall())
    
    cursor.close()
    release_db_connection(conn)
    
    return portfolios