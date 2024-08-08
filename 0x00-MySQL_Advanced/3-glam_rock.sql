-- This query lists all bands with Glam rock as their main style
-- and ranks them by their longevity (in descending order)

SELECT
    band_name,
    COALESCE(YEAR(CURDATE()) - formed, split - formed) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
