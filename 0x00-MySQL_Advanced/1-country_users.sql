-- Drops the 'users' table if it already exists
DROP TABLE IF EXISTS users;

-- Creates a table with unique users
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing primary key
    email VARCHAR(255) NOT NULL UNIQUE, -- Unique email address
    name VARCHAR(255), -- User's name
    country CHAR(2) NOT NULL DEFAULT 'US' -- Country code (default is 'US')
        CHECK (country IN ('US', 'CO', 'TN')) -- Allowed values: 'US', 'CO', 'TN'
);
