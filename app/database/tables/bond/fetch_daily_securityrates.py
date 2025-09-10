from datetime import date
from app.database.tables.user.get_distinct_user_bond_symbols import get_distinct_user_bond_symbols
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one
from app.api.get_eod_prices import get_eod_prices
from app.database.tables.bonddata.bonddata_exists import bonddata_exists
from flask import current_app
from app.database.helpers.execute_change_query import execute_change_query

def fetch_daily_securityrates():
    
    last_update = fetch_one("SELECT securities FROM status WHERE id = 1")[0]

    if last_update == date.today():
        # Already updated today → skip
        return

    query = "SELECT bondsymbol FROM bond"
    bonds = [i[0] for i in fetch_all(query=query)]
    
    rates = get_eod_prices(bonds)
    
    # Track results for bulk logging
    successful_fetches = 0
    failed_fetches = 0
    failed_symbols = []

    for bond_symbol, (rate, volume, trade_date) in rates.items():
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (bond_symbol,))[0]

        if not bond_id or not rate or not trade_date:
            # Track failed fetch
            failed_fetches += 1
            error_msg = "No data available"
            if not bond_id:
                error_msg = "Bond not found in database"
            elif not rate:
                error_msg = "No price data available"
            elif not trade_date:
                error_msg = "No trade date available"
            
            failed_symbols.append((bond_symbol, error_msg))
            continue

        # Track successful fetch
        successful_fetches += 1

        if bonddata_exists(bond_id, log_date=trade_date):
            execute_change_query("""
                UPDATE bonddata
                SET bondrate = %s, bondvolume = %s
                WHERE bondid = %s AND bonddatalogtime = %s
            """, (rate, volume, bond_id, trade_date))
        else:
            execute_change_query("""
                INSERT INTO bonddata (bondid, bondrate, bondvolume, bonddatalogtime)
                VALUES (%s, %s, %s, %s)
            """, (bond_id, rate, volume, trade_date))
    
    # Log bulk operation result
    try:
        from app.database.tables.api_fetch_logs.log_api_fetch import log_api_fetch
        
        if failed_fetches == 0:
            # All successful
            log_api_fetch('STOCK_FETCH_BULK', 'STOCK', 'SUCCESS', f'Successfully fetched {successful_fetches} stocks')
        elif successful_fetches == 0:
            # All failed
            log_api_fetch('STOCK_FETCH_BULK', 'STOCK', 'FAILED', f'Failed to fetch all {failed_fetches} stocks')
        else:
            # Partially successful
            log_api_fetch('STOCK_FETCH_BULK', 'STOCK', 'PARTIAL', f'Successfully fetched {successful_fetches} stocks, {failed_fetches} failed')
        
        # Log individual failures for failed fetches section
        for symbol, error_msg in failed_symbols:
            log_api_fetch(symbol, 'STOCK', 'FAILED', error_msg)
            
    except Exception as e:
        # Log to console if API logging fails (e.g., during setup)
        print(f"⚠️  API logging failed: {e}")
        pass

    # Update global status (when fetch was executed, not last trading date)
    execute_change_query("""
        UPDATE status SET securities = %s WHERE id = 1
    """, (date.today(),))
