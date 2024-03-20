#!/bin/bash

set -eo pipefail

CURRENT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


poetry run pylint --rcfile="$CURRENT_DIRECTORY"/../.pylintrc -j 0 "$CURRENT_DIRECTORY"/../app
poetry run black --line-length 120 "$CURRENT_DIRECTORY"/../app
poetry run mypy --implicit-reexport --show-error-codes  "$CURRENT_DIRECTORY"/../app
poetry run isort --profile black --line-length=120 "$CURRENT_DIRECTORY"/../app