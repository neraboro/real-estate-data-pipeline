import pandas as pd
import re
import psycopg2
import io

df = pd.read_csv('../data/offers.csv', sep=';', on_bad_lines='skip',encoding='utf-8')

clean_df = pd.DataFrame()


def clean_price(price_str):
    if pd.isna(price_str): return None
    digits = re.sub(r'\D', '', str(price_str))
    return int(digits) if digits else None

clean_df['price'] = df['Цена'].apply(clean_price)
clean_df['address'] = df['Адрес']

def clean_area(area_str):
    if pd.isna(area_str): return None
    first_part = str(area_str).split('/')[0]
    try:
        return float(first_part)
    except:
        return None

clean_df['square_meters'] = df['Площадь, м2'].apply(clean_area)


def get_minutes_to_subway(metro_str):
    if pd.isna(metro_str): return None
    match = re.search(r'(\d+)\s*мин', str(metro_str))
    if match:
        return int(match.group(1))
    return None

clean_df['subway'] = df['Метро']
clean_df['minutes_to_subway'] = df['Метро'].apply(get_minutes_to_subway)

clean_df['parking'] = df['Парковка'].fillna('Не указано')

clean_df['ceiling_height'] = pd.to_numeric(df['Высота потолков, м'], errors='coerce')
connection_config = {
    "host": "localhost",
    "database": "cian_database",
    "user": "postgres",
    "password": "1234",
    "port": "5432"
}
query = "INSERT INTO cian_table (price, address, square_meters, subway, minutes_to_subway,parking,ceiling_height) VALUES (%s, %s, %s, %s,%s,%s,%s);"
df = df.where(df.isna(), None)
data_to_insert = [tuple(x) for x in clean_df.to_numpy()]

try:
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS cian_table CASCADE;")
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cian_table (
                            id SERIAL PRIMARY KEY,
                            price BIGINT,
                            address TEXT,
                            square_meters FLOAT,
                            subway TEXT,
                            minutes_to_subway INT,
                            parking TEXT,
                            ceiling_height FLOAT
                        );
                    """)
            conn.commit()
            cursor.executemany(query, data_to_insert)
            conn.commit()
            print(f"Успешно загружено строк: {len(clean_df)}")
except Exception as e:
    print(f"Ошибка при загрузке: {e}")
