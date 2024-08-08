-- Drops the existing 'users' table if it exists
DROP TABLE IF EXISTS users;

-- Creates a new table named 'users' with the following columns:
--   id (INT, NOT NULL, AUTO_INCREMENT, PRIMARY KEY)
--   email (VARCHAR(255), NOT NULL, UNIQUE)
--   name (VARCHAR(255), nullable)
--   country (CHAR(2), NOT NULL, DEFAULT 'US', CHECK constraint)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    country CHAR(2) NOT NULL DEFAULT 'US' CONSTRAINT country_check CHECK (country IN ('US', 'CO', 'TN'))
);
