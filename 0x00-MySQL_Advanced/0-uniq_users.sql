-- Drops the 'users' table if it exists
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- Automatically incremented unique identifier for each user
    email VARCHAR(255) NOT NULL UNIQUE,
    -- Email address of the user, must be unique
    name VARCHAR(255) -- Name of the user
);
