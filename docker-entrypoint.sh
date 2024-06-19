#!/bin/sh

python manage.py collectstatic --no-input

exec gunicorn app:app --bind=0.0.0.0:8080