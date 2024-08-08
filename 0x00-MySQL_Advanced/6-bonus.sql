-- stored procedure AddBonus that adds a new
-- that adds a new correction for a student.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;

    -- Check if the project exists
    SELECT COUNT(id) INTO project_count
    FROM projects
    WHERE name = project_name;

    -- If the project doesn't exist, insert it into the projects table
    IF project_count = 0 THEN
        INSERT INTO projects(name)
        VALUES(project_name);
    END IF;

    -- Get the project ID
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- Insert the correction into the corrections table
    INSERT INTO corrections(user_id, project_id, score)
    VALUES (user_id, project_id, score);
END $$
DELIMITER ;
