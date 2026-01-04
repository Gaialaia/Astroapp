#!/bin/sh

wait_for_db() {

    DB_HOST="db"
    DB_PORT="5432" # Use 5432 for Postgres or 3306 for MySQL

    echo "Waiting for database at $DB_HOST:$DB_PORT..."
    # Loop until we can successfully connect to the database port
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.5s
    done

    echo "Database is ready! Continuing..."
}

wait_for_db

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 astroknow.wsgi:application