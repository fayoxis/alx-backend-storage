-- Retrieve bands with 'Glam rock' as their main style, sorted by their longevity (descending)
WITH cte AS (
  SELECT band_name,
         formed,
         COALESCE(split, YEAR(CURRENT_DATE())) AS split_year
  FROM metal_bands
  WHERE style LIKE '%Glam rock%'
)
SELECT band_name,
       (split_year - formed) AS lifespan
FROM cte
ORDER BY lifespan DESC;
