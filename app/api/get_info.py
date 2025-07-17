import yfinance as yf
import re

def get_info(symbol):
    """
    Fetches financial information for a given security symbol using yfinance.

    Args:
        symbol (str): The ticker symbol of the security.

    Returns:
        dict: A dictionary containing the financial information of the security.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        name = info.get('shortName', 'N/A')
        country = info.get('country', 'N/A')
        currency = info.get('currency', 'N/A')
        website = info.get('website', 'N/A')
        industry = info.get('industry', 'N/A')
        sector = info.get('sector', 'N/A')
        
        long_description = info.get('longBusinessSummary', 'N/A')
        
        # --- Extrahiere den ersten Satz für 'description' mittels regulärem Ausdruck ---
        description = "N/A"
        if long_description != 'N/A':
            # Muster: Finde Text bis zum ersten Punkt, Fragezeichen oder Ausrufezeichen,
            # gefolgt von einem Leerzeichen und einem Großbuchstaben (oder dem String-Ende).
            match = re.match(r'^(.*?[.!?])(?=\s+[A-Z]|$)', long_description, re.DOTALL)
            
            if match:
                description = match.group(1).strip() # Gruppe 1 fängt den Satz vor dem Lookahead
            else:
                # Falls kein passendes Satzende gefunden wird, nimm den gesamten Text.
                description = long_description.strip()

        # --- Kategorisierung ---
        category = None
        quote_type = info.get('quoteType', '').upper() # Immer in Großbuchstaben für den Vergleich
        type_disp = info.get('typeDisp', '').capitalize() # Ersten Buchstaben groß für Vergleich

        if quote_type == "EQUITY" or type_disp == "Equity":
            category = "Share"
        elif quote_type == "ETF" or type_disp == "Etf": # yfinance gibt oft 'Etf' zurück
            category = "ETF"
        elif quote_type == "MUTUALFUND" or type_disp == "Fund":
            category = "Managed Fund"
        # "Government Bond" bleibt hier unberücksichtigt, da es über yfinance nicht zuverlässig ermittelbar ist.


        security_data = {
            "symbol": symbol,
            "name": name,
            "country": country,
            "currency": currency,
            "website": website,
            "industry": industry,
            "sector": sector,
            "description": description,
            "category": category
        }

        return security_data

    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {} # Return an empty dict if an error occurs