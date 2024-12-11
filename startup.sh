#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn dndRestAPI.wsgi:application --bind 0.0.0.0:8080