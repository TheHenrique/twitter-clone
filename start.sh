#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec python manage.py runserver 0.0.0.0:${PORT:-8000}