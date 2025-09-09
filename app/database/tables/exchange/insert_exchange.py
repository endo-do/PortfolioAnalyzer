from app.database.helpers.execute_change_query import execute_change_query

def insert_exchanges():
    """
    Inserts a set of common exchanges with their region IDs.
    """
    # region IDs according to your list
    exchanges = exchanges = [
    
    # North America (1)
    ("New York Stock Exchange", 1),
    ("NASDAQ", 1),
    ("Cboe Global Markets", 1),
    ("Toronto Stock Exchange", 1),
    ("Mexican Stock Exchange", 1),

    # Europe (2)
    ("London Stock Exchange", 2),
    ("Euronext", 2),
    ("Deutsche Börse", 2),
    ("SIX Swiss Exchange", 2),
    ("Borsa Italiana", 2),
    ("Madrid Stock Exchange", 2),
    ("Euronext Paris", 2),
    ("Euronext Amsterdam", 2),
    ("Vienna Stock Exchange", 2),
    ("Athens Stock Exchange", 2),
    ("Warsaw Stock Exchange", 2),
    ("Moscow Exchange", 2),
    ("Prague Stock Exchange", 2),
    ("Irish Stock Exchange", 2),
    ("Budapest Stock Exchange", 2),
    ("Stockholm Stock Exchange", 2),
    ("Oslo Stock Exchange", 2),
    ("Helsinki Stock Exchange", 2),
    ("Copenhagen Stock Exchange", 2),
    ("Luxembourg Stock Exchange", 2),

    # South America (3)
    ("B3 Brasil Bolsa Balcão", 3),
    ("Buenos Aires Stock Exchange", 3),
    ("Santiago Stock Exchange", 3),
    ("Lima Stock Exchange", 3),
    ("Colombia Stock Exchange", 3),

    # Asia (4)
    ("Tokyo Stock Exchange", 4),
    ("Osaka Exchange", 4),
    ("Hong Kong Stock Exchange", 4),
    ("Shanghai Stock Exchange", 4),
    ("Shenzhen Stock Exchange", 4),
    ("Singapore Exchange", 4),
    ("Korea Exchange", 4),
    ("Taiwan Stock Exchange", 4),
    ("Bombay Stock Exchange", 4),
    ("National Stock Exchange of India", 4),
    ("Indonesia Stock Exchange", 4),
    ("Philippine Stock Exchange", 4),
    ("Thailand Stock Exchange", 4),
    ("Malaysia Stock Exchange", 4),
    ("Pakistan Stock Exchange", 4),
    ("Ho Chi Minh Stock Exchange", 4),

    # Africa (5)
    ("Johannesburg Stock Exchange", 5),
    ("Egyptian Exchange", 5),
    ("Casablanca Stock Exchange", 5),
    ("Nairobi Securities Exchange", 5),
    ("Nigeria Stock Exchange", 5),

    # Middle East (6)
    ("Saudi Exchange", 6),
    ("Dubai Financial Market", 6),
    ("Abu Dhabi Securities Exchange", 6),
    ("Qatar Stock Exchange", 6),
    ("Kuwait Stock Exchange", 6),

    # Oceania (7)
    ("Australian Securities Exchange", 7),
    ("New Zealand Exchange", 7),
    
    ("Other", 8)]


    query = """
    INSERT INTO exchange (exchangename, region)
    VALUES (%s, %s)
    """

    for symbol, region_id in exchanges:
        execute_change_query(query, (symbol, region_id))
    
    print(f"    ✅ Default exchanges inserted successfully")