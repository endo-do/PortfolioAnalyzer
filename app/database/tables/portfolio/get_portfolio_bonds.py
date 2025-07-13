from app.database.helpers.fetch_all import fetch_all

def get_portfolio_bonds(portfolio_id):
    query = """
            SELECT b.bondid, b.bondsymbol, b.bondname, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime, pb.quantity, c.currencycode
            FROM bond b
            JOIN bondcategory bc USING (bondcategoryid)
            JOIN bonddata bd ON b.bondid = bd.bondid
            JOIN (
                SELECT bondid, MAX(bonddatalogtime) AS maxlogtime
                FROM bonddata
                GROUP BY bondid
            ) latest ON bd.bondid = latest.bondid AND bd.bonddatalogtime = latest.maxlogtime
            JOIN portfolio_bond pb ON b.bondid = pb.bondid
            JOIN currency c ON c.currencyid = b.bondcurrencyid
            WHERE pb.portfolioid = %s
            """
    args = (portfolio_id,)
    bonds = fetch_all(query, args, dictionary=True)
    return bonds