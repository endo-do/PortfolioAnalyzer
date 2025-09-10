from app.database.helpers.fetch_all import fetch_all

def get_all_bonds(search=None, category_filter=None):
    query = """
        SELECT
            b.*,
            bc.bondcategoryname,
            COALESCE(CAST(bd.bondrate AS CHAR), 'N/A') AS bondrate,
            COALESCE(CAST(bd.bondvolume AS CHAR), 'N/A') AS bondvolume,
            COALESCE(DATE_FORMAT(bd.bonddatalogtime, '%Y-%m-%d'), 'N/A') AS bonddatalogtime,
            c.currencycode,
            r.region,
            s.sectorname,
            s.sectordisplayname
        FROM bond b
        JOIN bondcategory bc USING(bondcategoryid)
        LEFT JOIN (
            SELECT bondid, bondrate, bondvolume, bonddatalogtime
            FROM bonddata bd1
            WHERE bonddatalogtime = (
                SELECT MAX(bd2.bonddatalogtime)
                FROM bonddata bd2
                WHERE bd2.bondid = bd1.bondid
            )
        ) bd ON bd.bondid = b.bondid
        JOIN currency c ON c.currencyid = b.bondcurrencyid
        LEFT JOIN exchange e ON e.exchangeid = b.bondexchangeid
        LEFT JOIN region r ON r.regionid = e.region
        LEFT JOIN sector s ON s.sectorid = b.bondsectorid
        WHERE (%s IS NULL OR bondcategoryname = %s)
          AND (%s IS NULL OR (bondsymbol LIKE %s OR bondname LIKE %s))
        ORDER BY b.bondid;
    """

    search_term = f"%{search}%" if search else None
    params = (category_filter, category_filter, search, search_term, search_term)

    return fetch_all(query, params, dictionary=True)
