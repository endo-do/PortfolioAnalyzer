"""Handles interactions between the front- and backend"""


import mysql.connector
from flask_login import UserMixin
from config import DB_CONFIG
from datetime import datetime


def get_db_connection():
    """
    connect to db using details from config file

    Returns:
        connection to db
    """
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

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
    conn.close()

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
            if base != quote:
                pairs.append((base, quote))

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
    return cursor.fetchone() is not None

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
    return result[0] if result else None