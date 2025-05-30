USE portfolioanalyzer;

DELIMITER //

CREATE FUNCTION get_latest_exchangerate (
    in_fromcurrencyid INT,
    in_tocurrencyid INT
)
RETURNS FLOAT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE exchrate FLOAT;

    SELECT exchangerate INTO exchrate
    FROM exchangerates e
    WHERE e.fromcurrencyid = in_fromcurrencyid
      AND e.tocurrencyid = in_tocurrencyid
      AND e.exchangeratelogtime = (
          SELECT MAX(e2.exchangeratelogtime)
          FROM exchangerates e2
          WHERE e2.fromcurrencyid = in_fromcurrencyid
            AND e2.tocurrencyid = in_tocurrencyid
      );

    RETURN exchrate;

END //

DELIMITER ;