from app.database.helpers.fetch_all import fetch_all
from app.database.helpers.fetch_one import fetch_one

def get_region_breakdown(portfolio_id):
    """
    Fetches the regional breakdown for a given portfolio, based on the exchange region mapping.
    Bonds with unmapped exchanges or 'Unknown' are grouped into 'Others'.
    Values are returned in the portfolio's native currency.

    Args:
        portfolio_id (int): The ID of the portfolio.

    Returns:
        dict: A dictionary containing region values and percentages.
    """
    query = """
    SELECT
        COALESCE(er.region, 'Other') AS region,
        SUM(pb.quantity * bd.bondrate * 
            COALESCE((
                SELECT er.exchangerate
                FROM exchangerate er
                WHERE er.fromcurrencyid = b.bondcurrencyid
                  AND er.tocurrencyid = p.portfoliocurrencyid
                  AND er.exchangeratelogtime = (
                      SELECT MAX(er2.exchangeratelogtime)
                      FROM exchangerate er2
                      WHERE er2.fromcurrencyid = er.fromcurrencyid
                        AND er2.tocurrencyid = er.tocurrencyid
                  )
            ), 1.0)
        ) AS total_value
    FROM bond b
    LEFT JOIN exchange e ON b.bondexchangeid = e.exchangeid
    LEFT JOIN region er ON e.region = er.regionid
    LEFT JOIN portfolio_bond pb 
        ON pb.bondid = b.bondid AND pb.portfolioid = %s
    LEFT JOIN portfolio p ON p.portfolioid = pb.portfolioid
    LEFT JOIN (
        SELECT bd1.bondid, bd1.bondrate
        FROM bonddata bd1
        JOIN (
            SELECT bondid, MAX(bonddatalogtime) AS max_time
            FROM bonddata
            GROUP BY bondid
        ) latest
        ON bd1.bondid = latest.bondid AND bd1.bonddatalogtime = latest.max_time
    ) bd ON bd.bondid = b.bondid
    GROUP BY COALESCE(er.region, 'Other')
    HAVING SUM(pb.quantity * bd.bondrate * 
        COALESCE((
            SELECT er.exchangerate
            FROM exchangerate er
            WHERE er.fromcurrencyid = b.bondcurrencyid
              AND er.tocurrencyid = p.portfoliocurrencyid
              AND er.exchangeratelogtime = (
                  SELECT MAX(er2.exchangeratelogtime)
                  FROM exchangerate er2
                  WHERE er2.fromcurrencyid = er.fromcurrencyid
                    AND er2.tocurrencyid = er.tocurrencyid
              )
        ), 1.0)
    ) > 0
    ORDER BY total_value DESC;
    """

    args = (portfolio_id,)
    region_data = fetch_all(query=query, args=args, dictionary=True)

    # Convert values to float to avoid TypeError in templates
    breakdown = {f"{item['region']}_value": float(item['total_value'] or 0) for item in region_data}


    # Calculate total portfolio value
    total_value = sum(breakdown.values())

    # Calculate percentages (as float with 2 decimals)
    percentages = {
        key.replace('_value', '_percent'): round(float(value / total_value * 100) if total_value else 0, 2)
        for key, value in breakdown.items()
    }

    # Combine values and percentages
    breakdown.update(percentages)

    return breakdown