#!/usr/bin/env bash

mkdir instance
cp exemple_config.json /instance/config.json
cp exemple_config.py /instance/config.py


flask db init
flask db migrate
flask db upgrade
flask insert-db


cd /API-IMO
python run.py
