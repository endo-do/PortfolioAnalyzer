from app.database.tables.bond.insert_security_testdata import insert_test_stocks

def insert_default_stocks():
    """
    Inserts default stocks for the portfolio analyzer system.
    This includes major stocks from different regions and exchanges.
    """
    default_stocks = [
        # ETFs
        ("SPY", "New York Stock Exchange"),
        ("QQQ", "NASDAQ"),
        ("EEM", "Toronto Stock Exchange"),
        ("VWO", "New York Stock Exchange"),
        ("VGK", "Euronext"),
        ("EZU", "Euronext"),
        ("EWU", "London Stock Exchange"),
        ("EWQ", "Euronext"),
        ("EWJ", "Tokyo Stock Exchange"),
        ("EWT", "Taiwan Stock Exchange"),
        ("EWY", "Korea Exchange"),
        
        # North America
        ("AAPL", "NASDAQ"),
        ("GOOGL", "NASDAQ"),
        ("AMZN", "NASDAQ"),
        ("MSFT", "NASDAQ"),
        ("TSLA", "NASDAQ"),
        ("META", "NASDAQ"),
        ("NFLX", "NASDAQ"),
        ("JNJ", "New York Stock Exchange"),
        ("XOM", "New York Stock Exchange"),
        ("OR", "New York Stock Exchange"),
        ("NVDA", "NASDAQ"),

        # Europe
        ("SIE.DE", "Deutsche Börse"),
        ("BMW.DE", "Deutsche Börse"),
        ("AIR.DE", "Deutsche Börse"),
        ("SAP.DE", "Deutsche Börse"),
        ("SHELL.AS", "Euronext Amsterdam"),
        ("NESN.SW", "SIX Swiss Exchange"),
        ("VOD", "London Stock Exchange"),
        ("AZN", "London Stock Exchange"),
        ("ERIC", "Stockholm Stock Exchange"),
        ("SAN", "Madrid Stock Exchange"),

        # Asia
        ("7203.T", "Tokyo Stock Exchange"),
        ("6758.T", "Tokyo Stock Exchange"),
        ("9984.T", "Tokyo Stock Exchange"),
        ("0700.HK", "Hong Kong Stock Exchange"),
        ("9988.HK", "Hong Kong Stock Exchange"),
        ("601398.SS", "Shanghai Stock Exchange"),
        ("INFY", "National Stock Exchange of India"),
        ("005930.KS", "Korea Exchange"),
        ("035420.KS", "Korea Exchange"),
        ("2317.TW", "Taiwan Stock Exchange"),

        # Oceania
        ("BHP", "Australian Securities Exchange"),
        ("AIR", "New Zealand Exchange"),

        # South America
        ("PETR4.SA", "B3 Brasil Bolsa Balcão"),
        ("VALE3.SA", "B3 Brasil Bolsa Balcão"),

        # Africa
        ("NPN.JO", "Johannesburg Stock Exchange"),
        ("SOL.JO", "Johannesburg Stock Exchange"),

        # Middle East
        ("2222.SR", "Saudi Exchange")
    ]
    
    insert_test_stocks(default_stocks)
