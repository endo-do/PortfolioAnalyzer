USE portfolioanalyzer;

CREATE PROCEDURE get_portfolio(IN in_portfolioid INT)
BEGIN
    SELECT
        p.portfolioid,
        p.portfolioname,
        p.portfoliodescription,
        c.currencycode,
        ROUND((
            SELECT SUM(
                COALESCE(bd.bondrate, 0) * COALESCE(pb.quantity, 0) *
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
            )
            FROM portfolio_bond pb
            JOIN bond b ON pb.bondid = b.bondid
            JOIN bonddata bd ON bd.bondid = b.bondid
            WHERE pb.portfolioid = p.portfolioid
              AND bd.bonddatalogtime = (
                  SELECT MAX(bd2.bonddatalogtime)
                  FROM bonddata bd2
                  WHERE bd2.bondid = pb.bondid
              )
        ), 2) AS total_value
    FROM portfolio p
    JOIN currency c ON p.portfoliocurrencyid = c.currencyid
    WHERE p.portfolioid = in_portfolioid;

END;