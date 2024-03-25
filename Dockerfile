FROM python:3.11-slim

ENV PYTHONPATH /build

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /build
ENTRYPOINT ["/build/pipeline/docker_entrypoint.sh"]

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./.pylintrc .

RUN mkdir -p ./app && mkdir -p ./pipeline && mkdir -p ./tests && mkdir -p ./manifests

COPY ./app ./app
COPY ./pipeline ./pipeline
COPY ./docker-compose-ci.yml ./docker-compose-ci.yml
COPY ./manifests ./manifests

RUN poetry config virtualenvs.create false \
  && poetry update \
  && poetry install --no-interaction --no-ansi

RUN ./pipeline/install_dependencies.sh