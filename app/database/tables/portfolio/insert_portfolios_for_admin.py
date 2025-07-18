from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.fetch_one import fetch_one

def insert_portfolios_for_admin():
    query = """
    INSERT INTO portfolio (portfolioname, portfoliodescription, portfoliocurrencyid, userid)
    VALUES (%s, %s, %s, %s);
    """
    execute_change_query(query, ("Tech Giants", "Top 5 tech stocks", 1, 1))
    execute_change_query(query, ("Growth & ETFs", "Growth stocks and ETFs", 1, 1))

    portfolio1_id = fetch_one("SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", ("Tech Giants", 1))[0]
    portfolio2_id = fetch_one("SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", ("Growth & ETFs", 1))[0]

    # Insert bonds into portfolio 1
    symbols_portfolio1 = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
    for symbol in symbols_portfolio1:
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
        if bond_id:
            execute_change_query("INSERT INTO portfolio_bond (portfolioid, bondid, quantity) VALUES (%s, %s, %s)", (portfolio1_id, bond_id[0], 1))

    # Insert bonds into portfolio 2
    symbols_portfolio2 = ['META', 'NFLX', 'VTI', 'SPY', 'IEMG']
    for symbol in symbols_portfolio2:
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
        if bond_id:
            execute_change_query("INSERT INTO portfolio_bond (portfolioid, bondid, quantity) VALUES (%s, %s, %s)", (portfolio2_id, bond_id[0], 1))