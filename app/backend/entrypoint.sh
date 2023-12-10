#!/bin/sh
python3 manage.py wait_for_db
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py add_superuser 
python3 manage.py add_coins_to_db
python3 manage.py collectstatic --noinput
