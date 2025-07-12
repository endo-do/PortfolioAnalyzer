from app.database.db import fetch_one, call_procedure, execute_change_query
from app.database.connection import User
from flask import current_app
from app.api.twelve_data import get_eod_price

def get_user_by_id(user_id):
    query = 'SELECT userid, username, userpwd, is_admin FROM users WHERE userid = %s'
    result = fetch_one(query, (user_id,))
    if result:
        return User(id=result[0], username=result[1], password=result[2], is_admin=result[3])
    return None

def get_distinct_user_bond_isins(userid):
    rows = call_procedure("get_user_distinct_bond_isins", (userid,))
    return {row[0]: row[1] for row in rows}

def fetch_user_data(userid):
    bonds = get_distinct_user_bond_isins(userid)

    for bondid, symbol in bonds.items():
        # Check if bonddata exists
        exists = fetch_one('SELECT 1 FROM bonddata WHERE bondid = %s LIMIT 1', (bondid,))
        if exists:
            continue

        eod_data = get_eod_price(current_app.api_queue, symbol)
        if eod_data and 'close' in eod_data:
            execute_change_query(
                """
                INSERT INTO bonddata (bondid, bondrate, bonddatalogtime)
                VALUES (%s, %s, %s)
                """,
                (bondid, eod_data['close'], eod_data['datetime'])
            )
        else:
            print(symbol, ': ', eod_data)