# FIAP Hackathon

Manage employee's clock in/out

[![codecov](https://codecov.io/gh/higfonseca/fiap-hackathon/graph/badge.svg?token=8KDSI4TKGQ)](https://codecov.io/gh/higfonseca/fiap-hackathon)

<br>

**Turma 2SOAT - Grupo 25**

Lucas Leal de Oliveira Martins - rm349524 <br>
lucaslealm@gmail.com

Hígor Sampaio da Fonseca - rm349608 <br>
higfonseca@gmail.com

---

## Project Documentation

- [DDD](https://miro.com/app/board/uXjVM5vyjrM=/?share_link_id=894139570420)

## Main Technologies

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Postgres 15](https://www.postgresql.org/download/)

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Makefile](https://www.gnu.org/software/make/#download)
- [pre-commit](https://pre-commit.com/)
- [FIAP Local Development](https://github.com/higfonseca/fiap-local-development)

## API Docs

API documentation is available after starting the project, through:

```
http://localhost:8888/docs
```

## Installation and local development

### Environment preparation

To start the MongoDB container from the [FIAP Local Development](https://github.com/higfonseca/fiap-local-development)
project, run on `fiap-local-development` directory:

```
make start
```

### Run on Docker containers

After starting `fiap-local-development` containers, run:

```
make build
```

To start the application:

```
make start
```

## Useful commands

### Containers

Stop

```
make stop
```

Restart

```
make restart
```

### View application logs

```
make logs 
```

### Lint and prettify

```
make lint
```

### Access application container bash

```
make shell
```