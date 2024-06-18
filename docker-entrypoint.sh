#!/bin/sh

python manage.py collectstatic --no-input

exec gunicorn _conf.wsgi --bind=0.0.0.0:8080