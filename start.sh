#!/bin/sh

echo "Collecting static files..."
python astroknow/manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --chdir astroknow astroknow.wsgi:application