from app.database.helpers.execute_change_query import execute_change_query

def insert_exchanges():
    """
    Inserts a set of common exchanges with their region IDs.
    """
    # region IDs according to your list
    exchanges = [
        ('NMS', 1),        # NASDAQ
        ('NYSE', 1),       # New York Stock Exchange
        ('TSX', 1),        # Toronto Stock Exchange
        ('MEX', 1),        # Bolsa Mexicana de Valores
        ('B3', 3),         # Brasil Bolsa Balcão
        ('GER', 2),        # XETRA / Germany
        ('FRA', 2),        # Frankfurt Stock Exchange
        ('EBS', 2),        # SIX Swiss Exchange
        ('LSE', 2),        # London Stock Exchange
        ('EURONEXT', 2),   # Pan-European Exchange
        ('ASX', 7),        # Australian Securities Exchange
        ('NSE', 4),        # National Stock Exchange of India
        ('BSE', 4),        # Bombay Stock Exchange
        ('TSE', 4),        # Tokyo Stock Exchange
        ('HKG', 4),        # Hong Kong Stock Exchange
        ('KRX', 4),        # Korea Exchange
        ('JSE', 5),        # Johannesburg Stock Exchange
        ('TADAWUL', 6),    # Saudi Stock Exchange
        ('DXB', 6)        # Dubai Financial Market
    ]

    query = """
    INSERT INTO exchange (exchangesymbol, region)
    VALUES (%s, %s)
    """

    for symbol, region_id in exchanges:
        execute_change_query(query, (symbol, region_id))
