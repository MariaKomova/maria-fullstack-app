Проект "Full-Stack API Service"

Этот проект представляет собой микросервисный стек, запущенный с помощью Docker Compose, который состоит из трех основных компонентов: Nginx (Frontend/Proxy), Flask (Backend/API) и PostgreSQL (Database).

Архитектура

Frontend/Proxy: Контейнер frontend (Nginx) прослушивает порт 80, обрабатывает статические файлы и проксирует все запросы API на бэкенд (порт 8000).

Backend/API: Контейнер backend (Python/Flask) содержит логику CRUD (Create, Read, Update, Delete) и взаимодействует с базой данных.

Database: Контейнер db (PostgreSQL) хранит данные и инициализируется с помощью скрипта ./db/init.sql.

Запуск проекта

1. Требования

Для запуска проекта необходимы установленные Docker и Docker Compose.

2. Запуск стека

Выполните команду для сборки образов, запуска контейнеров и их работы в фоновом режиме:

docker-compose up -d --build


(Флаг --build гарантирует, что контейнер backend всегда будет использовать самую свежую версию кода.)

3. Проверка статуса

Убедитесь, что все три контейнера запущены:

docker-compose ps


4. Тестирование API (Smoke Test)

После запуска, API доступен по адресу http://localhost.

Метод

Конечная точка

Описание

Команда

POST

/items

Создание нового элемента.

curl -X POST http://localhost/items -H "Content-Type: application/json" -d '{"name": "Test Item", "description": "This works."}'

GET

/items

Получение всех элементов.

curl http://localhost/items

GET

/items/{id}

Получение элемента по ID.

curl http://localhost/items/1

PUT

/items/{id}

Обновление элемента.

curl -X PUT http://localhost/items/1 -H "Content-Type: application/json" -d '{"description": "Updated description"}'

DELETE

/items/{id}

Удаление элемента.

curl -X DELETE http://localhost/items/1

Устранение неисправностей

Ошибка аутентификации БД (FATAL): Произошло несоответствие паролей. Выполните полный сброс, чтобы удалить старый том БД: docker-compose down -v.

Ошибка 405/502: Проверьте frontend/nginx.conf на корректность порта (8000) и разрешения всех методов (GET|POST|PUT|DELETE|OPTIONS).
