UPDATE cian_table SET address = REPLACE(address,'Москва, ','');
UPDATE cian_table SET parking = NULL WHERE parking='Не указано';
UPDATE cian_table SET ceiling_height = NULL WHERE ceiling_height = 'NaN';
ALTER TABLE cian_table ADD price_per_meter FLOAT;
UPDATE cian_table SET price_per_meter = ROUND((price/square_meters)::numeric,2);

select * from cian_table