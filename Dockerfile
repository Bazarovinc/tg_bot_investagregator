# Используйте официальный Python образ
FROM python:3.10-slim

# Установите рабочую директорию
ENV UV_PROJECT_ENVIRONMENT=/usr/local
# Install poetry
RUN pip install uv

# Copy only the pyproject.toml and poetry.lock files to install dependencies first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --locked --no-dev

COPY ./main.py /code

COPY ./src /code/src
COPY ./migrations /code/migrations

# Укажите команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]