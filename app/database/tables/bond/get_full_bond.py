from app.database.helpers.fetch_one import fetch_one

def get_full_bond(bond_id):
    """
    Fetches detailed information about a bond, including its latest data entry.
    
    :param bond_id: The ID of the bond to fetch.
    :return: A dictionary containing bond details or None if not found.
    """
    query = """
    SELECT 
        b.bondid,
        b.bondsymbol,
        b.bondname,
        b.bonddescription,
        b.bondcountry,
        e.exchangesymbol,
        b.bondexchangeid,
        b.bondwebsite,
        b.bondindustry,
        b.bondsectorid,
        s.sectorname as bondsectorname,
        c.currencycode,
        c.currencyid as bondcurrencyid,
        bc.bondcategoryname,
        bc.bondcategoryid,
        bd.bondrate,
        bd.bonddatalogtime
    FROM bond b
    LEFT JOIN currency c ON b.bondcurrencyid = c.currencyid
    LEFT JOIN bondcategory bc ON b.bondcategoryid = bc.bondcategoryid
    LEFT JOIN exchange e on b.bondexchangeid = e.exchangeid
    LEFT JOIN sector s ON b.bondsectorid = s.sectorid
    LEFT JOIN bonddata bd ON bd.bondid = b.bondid
    WHERE b.bondid = %s
    ORDER BY bd.bonddatalogtime DESC
    LIMIT 1
    """
    bond = fetch_one(query, (bond_id,), dictionary=True)
    return bond if bond else None