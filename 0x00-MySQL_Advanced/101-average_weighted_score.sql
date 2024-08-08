-- Creates a stored procedure
-- that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users U
    JOIN (
        SELECT U.id, SUM(C.score * P.weight) / SUM(P.weight) AS w_avg
        FROM users U
        JOIN corrections C ON U.id = C.user_id
        JOIN projects P ON C.project_id = P.id
        GROUP BY U.id
    ) WA ON U.id = WA.id
    SET U.average_score = WA.w_avg;
END$$
DELIMITER ;
