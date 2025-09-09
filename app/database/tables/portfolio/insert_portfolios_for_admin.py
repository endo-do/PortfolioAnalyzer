from app.database.helpers.execute_change_query import execute_change_query
from app.database.helpers.fetch_one import fetch_one

def insert_portfolios_for_admin():
    print("    📊 Creating portfolios for admin user...")
    
    query = """
    INSERT INTO portfolio (portfolioname, portfoliodescription, portfoliocurrencyid, userid)
    VALUES (%s, %s, %s, %s);
    """
    # Create 3 portfolios
    print("    📁 Creating portfolio: Global Tech")
    execute_change_query(query, ("Global Tech", "Major tech companies from US, Europe, Asia", 1, 1))
    
    print("    📁 Creating portfolio: World Diversified")
    execute_change_query(query, ("World Diversified", "Companies from all over the world", 3, 1))
    
    print("    📁 Creating portfolio: European Leaders")
    execute_change_query(query, ("European Leaders", "Top European companies from various sectors", 2, 1))  # CHF currency id = 3

    portfolio1_id = fetch_one("SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", ("Global Tech", 1))[0]
    portfolio2_id = fetch_one("SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", ("World Diversified", 1))[0]
    portfolio3_id = fetch_one("SELECT portfolioid FROM portfolio WHERE portfolioname = %s AND userid = %s", ("European Leaders", 1))[0]
    
    print(f"    ✅ Portfolio IDs retrieved - Global Tech: {portfolio1_id}, World Diversified: {portfolio2_id}, European Leaders: {portfolio3_id}")

    # Portfolio 1: mostly North American tech
    print("    📈 Adding stocks to Global Tech portfolio...")
    symbols_portfolio1 = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX", "JNJ", "XOM", "NVDA"]
    for symbol in symbols_portfolio1:
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
        if bond_id:
            execute_change_query(
                "INSERT INTO portfolio_bond (portfolioid, bondid, quantity) VALUES (%s, %s, %s)",
                (portfolio1_id, bond_id[0], 1)
            )
            print(f"        ✅ {symbol}: Successfully added to Global Tech portfolio")
        else:
            print(f"        ❌ {symbol}: Could not be added to Global Tech portfolio - stock not found in database")

    # Portfolio 2: global companies
    print("    🌍 Adding stocks to World Diversified portfolio...")
    symbols_portfolio2 = ["SIE.DE", "OR", "NESN.SW", "VOD", "AZN", "ERIC", "SAN",
                          "7203.T", "6758.T", "9984.T", "601398.SS", "INFY", "JNJ", "XOM", "BHP", "0700.HK", "9988.HK", "CBA"]
    for symbol in symbols_portfolio2:
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
        if bond_id:
            execute_change_query(
                "INSERT INTO portfolio_bond (portfolioid, bondid, quantity) VALUES (%s, %s, %s)",
                (portfolio2_id, bond_id[0], 1)
            )
            print(f"        ✅ {symbol}: Successfully added to World Diversified portfolio")
        else:
            print(f"        ❌ {symbol}: Could not be added to World Diversified portfolio - stock not found in database")

    # Portfolio 3: Europe-focused
    print("    🇪🇺 Adding stocks to European Leaders portfolio...")
    symbols_portfolio3 = ["SIE.DE", "NESN.SW", "VOD", "AZN", "ERIC", "SAN", "SAP.DE", "BMW.DE", "AIR.DE"]
    for symbol in symbols_portfolio3:
        bond_id = fetch_one("SELECT bondid FROM bond WHERE bondsymbol = %s", (symbol,))
        if bond_id:
            execute_change_query(
                "INSERT INTO portfolio_bond (portfolioid, bondid, quantity) VALUES (%s, %s, %s)",
                (portfolio3_id, bond_id[0], 1)
            )
            print(f"    ✅ {symbol}: Successfully added to European Leaders portfolio")
        else:
            print(f"    ❌ {symbol}: Could not be added to European Leaders portfolio - stock not found in database")

    print("    ✅ Global test portfolios created successfully")
