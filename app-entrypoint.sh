#!/bin/sh
set -e

flask db upgrade
flask insert-db

python -m flask run
