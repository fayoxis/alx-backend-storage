-- Lists all bands with Glam rock as their main style, ranked by their longevity
-- script that lists all bands with Glam rock as their main style
SELECT
    band_name,
    COALESCE(split, 2022) - formed AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
