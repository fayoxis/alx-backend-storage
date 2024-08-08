-- Lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
    band_name,
    COALESCE(
        CASE
            WHEN split IS NULL THEN YEAR(CURRENT_DATE()) - formed
            ELSE split - formed
        END,
        0
    ) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
