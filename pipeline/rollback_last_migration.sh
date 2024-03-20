#!/bin/bash
set -eo pipefail

poetry run alembic downgrade -1