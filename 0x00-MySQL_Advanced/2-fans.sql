-- This query ranks the country origins of bands
-- ordered by the number of (non-unique) fans.

SELECT 
    origin, -- Country of origin
    SUM(fans) AS nb_fans -- Sum of fans for each origin (non-unique)
FROM 
    metal_bands
GROUP BY 
    origin -- Group the results by country of origin
ORDER BY 
    nb_fans DESC; -- Order the results by the number of fans in descending order
