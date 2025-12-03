import os
import time
import psycopg2

# Используем те же переменные окружения, что и в app.py
DB_HOST = os.environ.get('DATABASE_HOST', 'db')
DB_NAME = os.environ.get('DATABASE_NAME', 'devops_db')
DB_USER = os.environ.get('DATABASE_USER', 'devops_user')
DB_PASS = os.environ.get('DATABASE_PASSWORD', 'devops_password')

# SQL-команда для создания таблицы
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);
"""

print(f"Попытка подключиться к БД: {DB_HOST} / {DB_NAME}")

# Пробуем подключиться с таймаутом, так как БД может быть еще не готова
MAX_RETRIES = 10
DELAY = 3 # Задержка в секундах

conn = None
for i in range(MAX_RETRIES):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            connect_timeout=3
        )
        print("Подключение к БД установлено.")
        break
    except psycopg2.OperationalError as e:
        print(f"Попытка {i+1}/{MAX_RETRIES}: Ошибка подключения к БД. Ожидание {DELAY}с... ({e})")
        time.sleep(DELAY)
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        break

if conn is None:
    print("Ошибка: Не удалось подключиться к базе данных после всех попыток.")
    exit(1)

try:
    # Создаем курсор и выполняем команду CREATE TABLE
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    print("Таблица 'items' успешно создана или уже существовала.")

except Exception as e:
    print(f"Ошибка при создании таблицы: {e}")
    conn.rollback()
finally:
    if conn:
        conn.close()
        print("Соединение с БД закрыто.")
