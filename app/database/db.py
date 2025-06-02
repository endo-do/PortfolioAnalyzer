"""Handles interactions between the front- and backend"""


from app.database.connection import get_db_connection, release_db_connection
from datetime import date
from app.api.twelve_data import get_exchange_rate, get_eod_price
from app.database.get_data import get_all_currency_pairs, get_currency_code_by_id, get_distinct_user_bond_isins
from flask import current_app


def exchange_rate_exists_ondate(from_currency_id, to_currency_id, date):
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

def exchange_rate_exists(from_currency_id, to_currency_id):
    """
    Check if an exchange rate record exists for given currencies

    Args:
        cursor: Database cursor
        from_currency_id (int): currencyid of base currency
        to_currency_id (int): currencyid of quote currency

    Returns:
        bool: True if record exists, else False
    """
    query = """
        SELECT 1 FROM exchangerates
        WHERE fromcurrencyid = %s AND tocurrencyid = %s
        LIMIT 1
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (from_currency_id, to_currency_id))
    result = cursor.fetchone()
    cursor.close()
    release_db_connection(conn)
    
    return result is not None

def fetch_startup_data():
    """
    Fetches or calculates exchangerates for each currency if none are present in the db
    """

    currency_pairs = get_all_currency_pairs()
    conn = get_db_connection()
    cursor = conn.cursor()

    new_rates = {}

    for pair in currency_pairs:
        from_id, to_id = pair

        if exchange_rate_exists(from_id, to_id):
            continue

        if from_id == to_id:
            new_rates[(from_id, to_id)] = 1.0

        elif (to_id, from_id) in new_rates:
            rate = new_rates[(to_id, from_id)]
            new_rates[(from_id, to_id)] = 1 / rate

        else:
            rate_data = get_exchange_rate(
                current_app.api_queue,
                f"{get_currency_code_by_id(from_id)}/{get_currency_code_by_id(to_id)}"
            )
            new_rates[(from_id, to_id)] = rate_data["rate"]

    # Insert all collected rates
    for (from_id, to_id), rate in new_rates.items():
        cursor.execute("""
            INSERT INTO exchangerates
                (fromcurrencyid, tocurrencyid, exchangerate, exchangeratelogtime)
                VALUES (%s, %s, %s, %s)
        """, (from_id, to_id, rate, date.today()))

    conn.commit()
    cursor.close()
    release_db_connection(conn)

def fetch_user_data(userid):
    bonds = get_distinct_user_bond_isins(userid)
    conn = get_db_connection()
    cursor = conn.cursor()

    for id, symbol in bonds.items():
        cursor.execute("SELECT 1 FROM bonddata WHERE bondid = %s LIMIT 1", (id,))
        if cursor.fetchone():
            continue
        eod_data = get_eod_price(current_app.api_queue, symbol)
        if eod_data and "close" in eod_data:
            cursor.execute("""
                INSERT INTO bonddata (bondid, bondrate, bonddatalogtime)
                VALUES (%s, %s, %s)
            """, (id, eod_data["close"], eod_data["datetime"]))
        else:
            print(symbol, ": ", eod_data)
    conn.commit()
    cursor.close()
    release_db_connection(conn)