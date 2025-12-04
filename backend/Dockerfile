FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# ИСПОЛЬЗУЕМ GUNICORN И ОЖИДАЕМ БАЗУ ДАННЫХ
# wait-for-it.sh ждет, пока сервис 'db' будет доступен на порту 5432.
# Только после этого запускается Gunicorn.
CMD ["/usr/local/bin/wait-for-it.sh", "db:5432", "--timeout=30", "--", \
     "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
