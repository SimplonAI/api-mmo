#!/bin/sh

set -e
  
echo "Waiting for Postgres (10 seconds)..."
sleep 10

flask db upgrade
flask insert-db

python -m flask run
