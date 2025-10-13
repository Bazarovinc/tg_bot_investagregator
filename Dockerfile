# Используйте официальный Python образ
FROM python:3.10-slim

# Установите рабочую директорию
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV PYTHONPATH=/code
# Install poetry
RUN pip install uv

# Copy only the pyproject.toml and poetry.lock files to install dependencies first
RUN mkdir /code
WORKDIR /code/
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --locked --no-dev

COPY ./src /code/src
COPY ./entrypoint.sh /code
COPY ./alembic.ini /code
COPY ./migrations /code/migrations
COPY ./test_main.py /code
RUN chmod 777 /code/entrypoint.sh
## Укажите команду для запуска приложения
#CMD alembic upgrade head && python3 -m test_main