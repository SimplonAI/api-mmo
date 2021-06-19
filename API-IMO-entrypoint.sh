#!/usr/bin/env bash

mkdir instance
cp exemple_config.json /instance/config.json

flask db init
flask db migrate
flask db upgrade
flask insert-db
flask create-user

