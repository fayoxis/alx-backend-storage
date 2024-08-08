-- This trigger decreases the quantity of an item after a new order is added
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - (SELECT number FROM orders WHERE id = NEW.id)
    WHERE name = (SELECT item_name FROM orders WHERE id = NEW.id);
END$$
DELIMITER ;
