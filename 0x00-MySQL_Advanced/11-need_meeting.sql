-- Drops the existing view 'need_meeting' if it exists
DROP VIEW IF EXISTS need_meeting;

-- Creates a view 'need_meeting' that lists all students with a score below 80
-- and either no last_meeting record or a last_meeting older than one month
CREATE VIEW need_meeting AS
SELECT s.name
FROM students s
WHERE s.score < 80
  AND (s.last_meeting IS NULL
       OR s.last_meeting < DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH));
