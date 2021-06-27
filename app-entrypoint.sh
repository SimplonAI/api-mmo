#!/bin/sh
<<<<<<< HEAD
=======

>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
set -e
  
echo "Waiting for Postgres (10 seconds)..."
sleep 10

<<<<<<< HEAD
python3.9 -m flask db upgrade
python3.9 -m flask insert-db

python3.9 -m flask run
=======
flask db upgrade
flask insert-db

python -m flask run
>>>>>>> e13e2267f607ff2a7b6b3afbe4833bb4ea435def
