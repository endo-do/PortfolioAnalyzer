from app.database.helpers.fetch_all import fetch_all

def get_bonds(search=None, category_filter=None):
    query = """
        SELECT b.*, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime, c.currencycode
        FROM bond b JOIN bondcategory bc USING(bondcategoryid)
        JOIN (
            SELECT bondid, bondrate, bonddatalogtime
            FROM bonddata bd1 WHERE bonddatalogtime = (
            SELECT MAX(bd2.bonddatalogtime) FROM bonddata bd2
            WHERE bd2.bondid = bd1.bondid))
            bd ON bd.bondid = b.bondid
        JOIN currency c ON c.currencyid = b.bondcurrencyid
        WHERE (%s IS NULL OR bondcategoryname = %s)
        AND (%s IS NULL OR (bondsymbol LIKE %s OR bondname LIKE %s))
        ORDER BY b.bondid;
    """
    search_pattern = f"%{search}%" if search else None
    
    args = (
        category_filter, category_filter,
        search, search_pattern, search_pattern
    )
    
    return fetch_all(query, args, dictionary=True)