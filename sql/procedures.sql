USE portfolioanalyser;

drop PROCEDURE calculate_portfolio_value;
DELIMITER //

CREATE PROCEDURE calculate_portfolio_value(
    IN p_portfolioid INT,
    OUT total_value DECIMAL(15,5)
)
BEGIN
    DECLARE p_currencyid INT;

    -- Portfoliowährung ermitteln
    SELECT portfoliocurrencyid INTO p_currencyid
    FROM portfolios
    WHERE portfolioid = p_portfolioid;

    -- Gesamtwert berechnen (Anleihewert * Menge * Wechselkurs)
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
END //

DELIMITER ;
call calculate_portfolio_value(1, @totalvalue);

select @totalvalue;