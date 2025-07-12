from app.database.tables.user.get_distinct_user_bond_isins import get_distinct_user_bond_isins
from app.database.helpers.fetch_one import fetch_one
from app.api.get_eod_price import get_eod_price
from flask import current_app
from app.database.helpers.execute_change_query import execute_change_query

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