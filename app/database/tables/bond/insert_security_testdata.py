from datetime import date
from app.api.get_info import get_info
from app.api.get_eod import get_eod
from app.database.helpers.fetch_one import fetch_one
from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.execute_change_query import execute_change_query

def get_category_mapping():
        rows = fetch_all("SELECT bondcategoryid, bondcategoryname FROM bondcategory", dictionary=True)
        return {row['bondcategoryname']: row['bondcategoryid'] for row in rows}

def get_currency_mapping():
        rows = fetch_all("SELECT currencyid, currencycode FROM currency", dictionary=True)
        return {row['currencycode']: row['currencyid'] for row in rows}

def insert_test_stocks(symbols):
    """
    Inserts or updates stocks in the DB using your existing functions get_info and get_eod.
    
    Args:
        symbols (list of str): List of ticker symbols to insert.
    """

    category_map = get_category_mapping()
    currency_map = get_currency_mapping()

    def map_category_to_id(category_name):
        return category_map.get(category_name, category_map.get('Other'))

    def map_currency_to_id(currency_code):
        return currency_map.get(currency_code, currency_map.get('USD'))


    for symbol_data in symbols:
        # Extract symbol and exchange from the array
        symbol = symbol_data[0]  # stock ticker symbol
        exchange_name = symbol_data[1]  # exchange market name
        
        info = get_info(symbol)
        eod, volume, trade_date = get_eod(symbol)

        # fallback if info is empty (error handling)
        if not info:
            print(f"    ❌ {symbol} : no info found - check the ticker symbol again")
            continue

        bondname = info.get("name", "")
        bondcategoryid = map_category_to_id(info.get("category"))
        bondcurrencyid = map_currency_to_id(info.get("currency"))
        bondcountry = info.get("country", "")
        bondwebsite = info.get("website", "")
        bondindustry = info.get("industry", "")
        bondsector = info.get("sector", "")
        bondsectorid = fetch_one("""SELECT sectorid FROM sector WHERE sectorname = %s""", (bondsector,), dictionary=True)
        bondsectorid = bondsectorid['sectorid'] if bondsectorid else None
        bonddescription = info.get("description", "")
        
        # Get exchange ID using the provided exchange name
        bondexchangeid = fetch_one("""SELECT exchangeid FROM exchange WHERE exchangename = %s""", (exchange_name,), dictionary=True)
        if bondexchangeid:
            bondexchangeid = bondexchangeid['exchangeid']
        else:
            print(f"    ❌ {symbol} : Exchange '{exchange_name}' not found in database")
            bondexchangeid = None
            continue  # Skip this symbol if exchange not found
        
        # Insert new bond
        query = """
            INSERT INTO bond (
                bondname, bondsymbol, bondcategoryid, bondcurrencyid,
                bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_change_query(query, (
            bondname, symbol, bondcategoryid, bondcurrencyid,
            bondcountry, bondexchangeid, bondwebsite, bondindustry, bondsectorid, bonddescription))

        bond_row = fetch_one("""SELECT bondid FROM bond WHERE bondsymbol = %s""", (symbol,), dictionary=True)
        if not bond_row:
            print(f"    ❌ {symbol} : Error - bond was not inserted properly")
            continue  # skip to the next symbol

        bondid = bond_row['bondid']

        if eod is not None:
            query = """INSERT INTO bonddata (bondid, bonddatalogtime, bondrate, bondvolume) VALUES (%s, %s, %s, %s)"""
            execute_change_query(query, (bondid, trade_date, eod, volume))
            volume_text = f", volume: {volume:,}" if volume else ""
            print(f"    ✅ {symbol} ({exchange_name}): Successfully inserted with price data ({eod:.2f}{volume_text})")
        else:
            print(f"    ❌ {symbol} ({exchange_name}): No price data found - check the ticker symbol again")

    # Note: Don't update securities status here - this is just inserting test data
    # The status will be updated when actual live data is fetched by fetch_daily_securityrates

    print("    ✅ Finished inserting/updating test stocks.")
