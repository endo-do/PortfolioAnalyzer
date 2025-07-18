USE portfolioanalyzer;

CREATE TRIGGER reset_eod_flag_after_security_update
AFTER UPDATE ON bond
FOR EACH ROW
BEGIN
    UPDATE status SET securities = NULL WHERE id = 1;
END;