-- Lists all bands with Glam rock as their main style, ranked by their longevity
-- script that lists all bands with Glam rock as their main style
SELECT DISTINCT
    `band_name`,
    COALESCE(`split` - `formed`, 2024 - `formed`) AS `lifespan`
FROM `metal_bands`
WHERE `style` LIKE '%Glam rock%'
ORDER BY `lifespan` DESC;
