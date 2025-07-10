from app.database.get_data import fetch_all, fetch_one

def get_bondcategory_totals_by_portfolio(portfolio_id):
    category_rows = fetch_all('SELECT bondcategoryid FROM bondcategories')
    bondcategories = [row[0] for row in category_rows]
    totals = {}
    for bondcategoryid in bondcategories:
        row = fetch_one('SELECT get_bondcategory_value(%s, %s)', (portfolio_id, bondcategoryid))
        totals[bondcategoryid] = row[0] if row else 0
    return totals

def get_portfolio_by_id(portfolio_id):
    query = """
        SELECT portfolioname, portfoliodescription, currencycode 
        FROM portfolios p JOIN currencies c on c.currencyid = p.portfoliocurrencyid
        WHERE portfolioid = %s;"""
    args = (portfolio_id,)
    portfolio = fetch_one(query, args, dictionary=True)
    return portfolio

def get_portfolio_bonds(portfolio_id):
    query = """
            SELECT b.symbol, b.bondname, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime
            FROM bonds b
            JOIN bondcategories bc USING (bondcategoryid)
            JOIN bonddata bd ON b.bondid = bd.bondid
            JOIN (
                SELECT bondid, MAX(bonddatalogtime) AS maxlogtime
                FROM bonddata
                GROUP BY bondid
            ) latest ON bd.bondid = latest.bondid AND bd.bonddatalogtime = latest.maxlogtime
            JOIN portfolios_bonds pb ON b.bondid = pb.bondid
            WHERE pb.portfolioid = %s
            """
    args = (portfolio_id,)
    bonds = fetch_all(query, args, dictionary=True)
    return bonds