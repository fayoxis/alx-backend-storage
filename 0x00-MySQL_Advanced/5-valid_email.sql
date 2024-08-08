DELIMITER $$
CREATE TRIGGER reset_validation
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- This trigger resets the valid_email attribute to 0 when the email is changed
    -- This ensures that the new email address needs to be validated
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$
DELIMITER ;
