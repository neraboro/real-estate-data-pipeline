SELECT * FROM cian_table WHERE price_per_meter < (SELECT AVG(price_per_meter) FROM cian_table) AND subway LIKE '%пешком%'
ORDER BY minutes_to_subway,square_meters DESC LIMIT 10