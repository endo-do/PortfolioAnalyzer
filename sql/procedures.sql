USE portfolioanalyser;

DELIMITER //

CREATE PROCEDURE calculate_portfolio_value(
    IN p_portfolioid INT,
    OUT total_value DECIMAL(15,5)
)
BEGIN
    DECLARE p_currencyid INT;

    -- Portfolio currency
    SELECT portfoliocurrencyid INTO p_currencyid
    FROM portfolios
    WHERE portfolioid = p_portfolioid;

    -- Total Value (Bondrate * Quantity * Exchangerate)
    SELECT
        SUM(
            bd.bondrate * pb.quantity * 
            (
                SELECT er.exchangerate
                FROM exchangerates er
                WHERE er.fromcurrencyid = b.bondcurrencyid
                  AND er.tocurrencyid = p_currencyid
                  AND er.exchangeratelogtime = ( 
                      SELECT MAX(exchangeratelogtime)
                      FROM exchangerates
                      WHERE fromcurrencyid = er.fromcurrencyid
                        AND tocurrencyid = er.tocurrencyid
                  )
            )
        ) INTO total_value
    FROM portfolios_bonds pb
    JOIN bonds b ON pb.bondid = b.bondid
    JOIN bonddata bd ON pb.bondid = bd.bondid
    WHERE
        bd.bonddatalogtime = (
            SELECT MAX(bonddatalogtime)
            FROM bonddata
            WHERE bondid = pb.bondid
        )
      AND pb.portfolioid = p_portfolioid;
END //;

DELIMITER ;