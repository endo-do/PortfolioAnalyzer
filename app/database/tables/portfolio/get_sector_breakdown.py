from app.database.helpers.fetch_all import fetch_all

def get_sector_breakdown(portfolio_id):
    """
    Fetches the sector breakdown for a given portfolio, including bonds without a sector.

    Args:
        portfolio_id (int): The ID of the portfolio.

    Returns:
        dict: A dictionary containing sector values and percentages.
    """
    query = """
    SELECT
        s.sectorname AS sector,
        SUM(pb.quantity * bd.bondrate) AS total_value
    FROM bond b
    LEFT JOIN sector s ON b.bondsectorid = s.sectorid
    LEFT JOIN portfolio_bond pb ON pb.bondid = b.bondid AND pb.portfolioid = %s
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
    GROUP BY s.sectorname
    ORDER BY total_value DESC;
    """

    args = (portfolio_id,)
    sector_data = fetch_all(query=query, args=args, dictionary=True)

    # Convert values to float to avoid TypeError in templates
    breakdown = {f"{item['sector'].lower()}_value": float(item['total_value'] or 0) for item in sector_data}

    # Calculate total portfolio value
    total_value = sum(breakdown.values())

    # Calculate percentages (as float with 2 decimals)
    percentages = {
        sector.replace('_value', '_percent'): round(float(value / total_value * 100) if total_value else 0, 2)
        for sector, value in breakdown.items()
    }

    # Combine values and percentages
    breakdown.update(percentages)

    return breakdown
