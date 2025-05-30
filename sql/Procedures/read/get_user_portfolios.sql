USE portfolioanalyzer;

DELIMITER //

CREATE PROCEDURE get_user_portfolios(IN p_userid INT)
BEGIN
    SELECT
        p.portfolioid,
        p.portfolioname,
        p.portfoliodescription,
        c.currencycode,
        ROUND((
            SELECT SUM(
                bd.bondrate * pb.quantity *
                (
                    SELECT er.exchangerate
                    FROM exchangerates er
                    WHERE er.fromcurrencyid = b.bondcurrencyid
                      AND er.tocurrencyid = p.portfoliocurrencyid
                      AND er.exchangeratelogtime = (
                          SELECT MAX(er2.exchangeratelogtime)
                          FROM exchangerates er2
                          WHERE er2.fromcurrencyid = er.fromcurrencyid
                            AND er2.tocurrencyid = er.tocurrencyid
                      )
                )
            )
            FROM portfolios_bonds pb
            JOIN bonds b ON pb.bondid = b.bondid
            JOIN bonddata bd ON bd.bondid = b.bondid
            WHERE pb.portfolioid = p.portfolioid
              AND bd.bonddatalogtime = (
                  SELECT MAX(bd2.bonddatalogtime)
                  FROM bonddata bd2
                  WHERE bd2.bondid = pb.bondid
              )
        ), 2) AS total_value
    FROM portfolios p
    JOIN currencies c ON p.portfoliocurrencyid = c.currencyid
    WHERE p.userid = p_userid;

END //

DELIMITER ;