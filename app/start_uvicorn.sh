#!/bin/bash

set -e

echo "Activating virtual environment..."
. .venv/bin/activate

echo "Starting Uvicorn..."
exec uvicorn --workers 1 --host 0.0.0.0 --port 8000 app.main:app
