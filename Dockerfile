FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей для PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry и зависимостей
RUN pip install --no-cache-dir poetry==1.8.2

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

# Копирование проекта
COPY . .

# Создание пустых директорий для media и static
RUN mkdir -p /app/media /app/static

# Открываем порт
EXPOSE 8000
