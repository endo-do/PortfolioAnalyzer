from app.database.db import fetch_all

def get_bonds(search=None, category_filter=None):
    query = """
        SELECT b.*, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime, c.currencycode
        FROM bonds b JOIN bondcategories bc USING(bondcategoryid)
        JOIN (
            SELECT bondid, bondrate, bonddatalogtime
            FROM bonddata bd1 WHERE bonddatalogtime = (
            SELECT MAX(bd2.bonddatalogtime) FROM bonddata bd2
            WHERE bd2.bondid = bd1.bondid))
            bd ON bd.bondid = b.bondid
        JOIN currencies c ON c.currencyid = b.bondcurrencyid
        WHERE (%s IS NULL OR bondcategoryname = %s)
        AND (%s IS NULL OR (symbol LIKE %s OR bondname LIKE %s))
        ORDER BY b.bondid;
    """
    
    # Prepare args for the placeholders
    # For search, we use `%search%` for LIKE pattern matching if search is given
    search_pattern = f"%{search}%" if search else None
    
    args = (
        category_filter, category_filter,
        search, search_pattern, search_pattern
    )
    
    return fetch_all(query, args, dictionary=True)