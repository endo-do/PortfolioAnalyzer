USE portfolioanalyzer;

DELIMITER //

CREATE FUNCTION get_bondcategory_value(
    p_portfolioid INT,
    b_bondcategoryid INT
)
RETURNS DECIMAL(15,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_value DECIMAL(15,2);

    SELECT ROUND(SUM(
        bd.bondrate * pb.quantity *
        (
            SELECT er.exchangerate
            FROM exchangerates er
            WHERE er.fromcurrencyid = b.bondcurrencyid
              AND er.tocurrencyid = (
                  SELECT portfoliocurrencyid FROM portfolios WHERE portfolioid = p_portfolioid
              )
              AND er.exchangeratelogtime = (
                  SELECT MAX(er2.exchangeratelogtime)
                  FROM exchangerates er2
                  WHERE er2.fromcurrencyid = er.fromcurrencyid
                    AND er2.tocurrencyid = er.tocurrencyid
              )
        )
    ), 2)
    INTO total_value
    FROM portfolios_bonds pb
    JOIN bonds b ON pb.bondid = b.bondid
    JOIN bonddata bd ON bd.bondid = b.bondid
    WHERE pb.portfolioid = p_portfolioid
      AND b.bondcategoryid = b_bondcategoryid
      AND bd.bonddatalogtime = (
          SELECT MAX(bd2.bonddatalogtime)
          FROM bonddata bd2
          WHERE bd2.bondid = pb.bondid
      );

    RETURN total_value;
END //

DELIMITER ;