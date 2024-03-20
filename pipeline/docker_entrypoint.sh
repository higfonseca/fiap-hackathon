#!/bin/bash

set -eo pipefail

COMMAND=${1:-"web"}
CURRENT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRIPT_TO_RUN="$CURRENT_DIRECTORY/$COMMAND.sh"
COMMAND_ARGS=${2}

if [[ -f "$SCRIPT_TO_RUN" ]]; then
  echo "Script found. Executing..."
  exec "$SCRIPT_TO_RUN" "$COMMAND_ARGS"
else
  echo "Script ($SCRIPT_TO_RUN) not found. Starting application instead..."
  exec uvicorn app.main:app --reload --port 8800 --host 0.0.0.0
fi