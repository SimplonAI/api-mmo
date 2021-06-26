#!/bin/sh
set -e
  
echo "Waiting for Postgres (10 seconds)..."
sleep 10

python3.9 -m flask db upgrade
python3.9 -m flask insert-db

python3.9 -m flask run
