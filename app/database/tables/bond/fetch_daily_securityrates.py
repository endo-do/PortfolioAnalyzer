from app.database.tables.user.get_distinct_user_bond_symbols import get_distinct_user_bond_symbols
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.api.get_eod_prices import get_eod_prices
from app.database.tables.bonddata.bonddata_exists import bonddata_exists
from flask import current_app
from app.database.helpers.execute_change_query import execute_change_query
from datetime import date

def fetch_daily_securityrates():
    
    last_update = fetch_one("SELECT securities FROM update_status WHERE id = 1")[0]

    if last_update == date.today():
        print("Securities already updated today, skipping.")
        return

    print("Fetching today's security rates...")
    
    query = """SELECT bondsymbol FROM bond"""
    bonds = [i[0] for i in fetch_all(query=query)]
    
    rates = get_eod_prices(bonds)

    for bond_symbol, rate in rates.items():
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bond_symbol,))[0]

        if not bond_id or not rate:
            continue

        if bonddata_exists(bond_id, log_date=date.today()):
            execute_change_query("""
                UPDATE bonddata
                SET bondrate = %s
                WHERE bondid = %s AND bonddatalogtime = %s
            """, (rate, bond_id, date.today()))
        else:
            execute_change_query("""
                INSERT INTO bonddata (bondid, bondrate, bonddatalogtime)
                VALUES (%s, %s, %s)
            """, (bond_id, rate, date.today()))

    # Update global status
    execute_change_query("""
        UPDATE update_status SET securities = %s WHERE id = 1""",
        (date.today(),))
