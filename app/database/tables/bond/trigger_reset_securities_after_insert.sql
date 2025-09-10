CREATE TRIGGER reset_eod_flag_after_security_insert
AFTER INSERT ON bond
FOR EACH ROW
BEGIN
    UPDATE status SET securities = NULL WHERE id = 1;
END;