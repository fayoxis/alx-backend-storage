-- This function, SafeDiv, performs division of two integers.
-- If the divisor (second number) is non-zero, it returns the quotient.
-- If the divisor is zero, it returns 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv(dividend INT, divisor INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE quotient FLOAT DEFAULT 0;

    IF divisor <> 0 THEN
        SET quotient = dividend / divisor;
    END IF;

    RETURN quotient;
END$$
DELIMITER ;
