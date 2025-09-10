CREATE TRIGGER reset_exchangerate_flag_after_currency_insert
AFTER INSERT ON currency
FOR EACH ROW
BEGIN
    UPDATE status
    SET exchangerates = NULL WHERE id = 1;
END;