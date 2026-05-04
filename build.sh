#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn cyberdu.wsgi:application --bind 0.0.0.0:8000