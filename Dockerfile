FROM python:3.11-slim

ENV PYTHONPATH /build

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /build
ENTRYPOINT ["/build/pipeline/docker_entrypoint.sh"]

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./.pylintrc .
COPY ./alembic.ini .
COPY ./app/infrastructure/persistence/alembic ./alembic

RUN mkdir -p ./app && mkdir -p ./pipeline && mkdir -p ./tests

COPY ./app ./app
COPY ./pipeline ./pipeline

RUN poetry config virtualenvs.create false \
  && poetry update \
  && poetry install --no-interaction --no-ansi

RUN ./pipeline/install_dependencies.sh