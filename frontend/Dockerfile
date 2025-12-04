FROM nginx:alpine

# 1. Удаляем стандартный конфиг Nginx
RUN rm /etc/nginx/conf.d/default.conf

# 2. Копируем наш кастомный конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 3. КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Обеспечиваем, что наш index.html заменит дефолтный
# Сначала очищаем корневую папку Nginx от всего контента базового образа
# (включая дефолтный index.html, который вы сейчас видите).
RUN rm -rf /usr/share/nginx/html/*

# 4. Копируем все файлы нашего фронтенда (включая index.html и любые CSS/JS/активы),
# которые находятся в контексте сборки, в папку, которую Nginx использует как корень.
COPY . /usr/share/nginx/html
