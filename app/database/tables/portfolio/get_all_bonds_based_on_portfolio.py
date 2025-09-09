from app.database.helpers.fetch_all import fetch_all

def get_all_bonds_based_on_portfolio(portfolio_id):
    query = """
        SELECT 
            b.bondid, 
            b.bondsymbol, 
            b.bondname, 
            bc.bondcategoryname, 
            bd.bondrate, 
            bd.bonddatalogtime, 
            COALESCE(pb.quantity, 0) AS quantity, 
            c.currencycode,
            r.region,
            s.sectorname,
            s.sectordisplayname
        FROM bond b
        JOIN bondcategory bc USING (bondcategoryid)
        JOIN bonddata bd ON b.bondid = bd.bondid
        JOIN (
            SELECT bondid, MAX(bonddatalogtime) AS maxlogtime
            FROM bonddata
            GROUP BY bondid
        ) latest ON bd.bondid = latest.bondid AND bd.bonddatalogtime = latest.maxlogtime
        LEFT JOIN portfolio_bond pb 
            ON b.bondid = pb.bondid AND pb.portfolioid = %s
        JOIN currency c ON c.currencyid = b.bondcurrencyid
        LEFT JOIN exchange e ON e.exchangeid = b.bondexchangeid
        LEFT JOIN region r ON r.regionid = e.region
        LEFT JOIN sector s ON s.sectorid = b.bondsectorid
    """
    args = (portfolio_id,)
    bonds = fetch_all(query, args, dictionary=True)
    return bonds