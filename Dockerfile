# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry версии 1.8.3
ENV POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip && pip install poetry==${POETRY_VERSION}

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости без разработки
RUN poetry install --no-dev --no-interaction --no-ansi

# Копируем все файлы проекта в контейнер
COPY . .

# Удаляем ненужные файлы и очищаем кэш
RUN apt-get purge -y --auto-remove gcc && rm -rf /var/lib/apt/lists/*

# ENTRYPOINT позволяет передавать команды через docker-compose.yml или docker run
ENTRYPOINT ["sh", "-c"]
