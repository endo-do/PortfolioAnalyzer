from app.database.helpers.fetch_all import fetch_all

def get_portfolio_bonds(portfolio_id, base_currency_code='USD'):
    query = """
            SELECT b.bondid, b.bondsymbol, b.bondname, bc.bondcategoryname, bd.bondrate, bd.bonddatalogtime, pb.quantity, c.currencycode,
                   c.currencyid, base_c.currencyid as base_currency_id,
                   CASE 
                       WHEN c.currencycode = %s THEN 1.0
                       ELSE get_latest_exchangerate(c.currencyid, base_c.currencyid)
                   END as exchange_rate_to_base
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
            CROSS JOIN currency base_c ON base_c.currencycode = %s
            WHERE pb.portfolioid = %s
            """
    args = (base_currency_code, base_currency_code, portfolio_id)
    bonds = fetch_all(query, args, dictionary=True)
    
    # Convert decimal.Decimal values to float to avoid TypeError in templates
    for bond in bonds:
        if 'exchange_rate_to_base' in bond and bond['exchange_rate_to_base'] is not None:
            bond['exchange_rate_to_base'] = float(bond['exchange_rate_to_base'])
        if 'bondrate' in bond and bond['bondrate'] is not None:
            bond['bondrate'] = float(bond['bondrate'])
        if 'quantity' in bond and bond['quantity'] is not None:
            bond['quantity'] = float(bond['quantity'])
    
    return bonds