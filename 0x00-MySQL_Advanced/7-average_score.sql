-- Drops the existing ComputeAverageScoreForUser stored procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Defines a new delimiter for the stored procedure
DELIMITER $$

-- Creates a stored procedure ComputeAverageScoreForUser that 
-- computes and stores the average score for a student
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    -- Declares and initializes variables
    DECLARE total_score INT DEFAULT 0;
    DECLARE projects_count INT DEFAULT 0;

    -- Calculates the total score for the given user
    SELECT SUM(score)
        INTO total_score
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Counts the number of projects for the given user
    SELECT COUNT(*)
        INTO projects_count
        FROM corrections
        WHERE corrections.user_id = user_id;

    -- Updates the average_score column in the users table for the given user
    UPDATE users
        SET users.average_score = IF(projects_count = 0, 0, total_score / projects_count)
        WHERE users.id = user_id;
END $$

-- Resets the delimiter to the default
DELIMITER ;
