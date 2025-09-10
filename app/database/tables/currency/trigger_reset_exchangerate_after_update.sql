CREATE TRIGGER reset_exchangerate_flag_after_currency_update
AFTER UPDATE ON currency
FOR EACH ROW
BEGIN
    UPDATE status
    SET exchangerates = NULL WHERE id = 1;
END;