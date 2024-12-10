#!/bin/sh

echo "=== Running Migrations ==="
python manage.py migrate

echo "=== Starting Django Server ==="
exec python manage.py runserver 0.0.0.0:8000
