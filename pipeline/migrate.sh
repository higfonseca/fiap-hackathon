#!/bin/bash
set -eo pipefail

poetry run python app/infrastructure/persistence/create_database.py

poetry run alembic upgrade head