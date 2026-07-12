import subprocess
import psycopg2

import sys

def run_python_file(filename):
    print(f'Запуск {filename}')
    subprocess.run([sys.executable, filename], check=True)
def run_sql_file(filename):
    print(f'Выполнение {filename}')
    connection_config = {
        "host": "localhost",
        "database": "cian_database",
        "user": "postgres",
        "password": "1234",
        "port": "5432"
    }
    with open(filename, 'r', encoding='utf-8') as file:
        sql = file.read()
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
print("=== ETL PIPELINE START ===")
run_python_file("main.py")
run_sql_file("../sql/redacted schema.sql")
run_python_file("analysis.py")
print("=== ETL PIPELINE FINISHED ===")