#!/bin/sh
set -e
  
echo "Waiting for Postgres (10 seconds)..."
sleep 10

python3.9 -m flask db upgrade
if [ ! -f ".db-initialized" ]; then
    python3.9 -m flask insert-db
    echo "initialized" > .db-initialized
fi
python3.9 -m gunicorn --workers=2 'app:create_app()' -b :5000
