FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY drmooha/ /app/drmooha/
COPY mooha/ /app/mooha/
COPY manage.py /app/

# Создание директорий для статических файлов и медиа
RUN mkdir -p /app/static /app/media

# Открытие порта
EXPOSE 8000

# Создание скрипта запуска
RUN echo '#!/bin/bash\n\
python /app/manage.py wait_for_db\n\
python /app/manage.py migrate\n\
python /app/manage.py runserver 0.0.0.0:8000 --noreload' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

# Запуск приложения
CMD ["/app/entrypoint.sh"] 