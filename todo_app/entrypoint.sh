#!/bin/bash
set -e

python3 manage.py makemigrations
python3 manage.py migrate

if [ "$DJANGO_SUPERUSER_TG_ID" ]; then
    python manage.py createsuperuser --no-input --tg_id "$DJANGO_SUPERUSER_TG_ID" || true
fi

exec "$@"
