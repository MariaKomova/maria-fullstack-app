# Базовый образ Python
FROM python:3.11-slim

# Установка зависимостей PostgreSQL (для Psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем код и устанавливаем Flask и Psycopg2
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Команда запуска
CMD ["python", "app.py"]
