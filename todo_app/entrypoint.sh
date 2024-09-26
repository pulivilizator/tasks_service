#!/bin/bash
set -e

python3 manage.py makemigrations
python3 manage.py migrate

if [ "$DJANGO_SUPERUSER_TG_ID" ]; then
    python manage.py createsuperuser --no-input --username "$DJANGO_SUPERUSER_TG_ID" --first_name "$DJANGO_SUPERUSER_FIRST_NAME" --username "$DJANGO_SUPERUSER_USERNAME" || true
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(tg_id=$DJANGO_SUPERUSER_TG_ID); user.set_password('$DJANGO_SUPERUSER_PASSWORD'); user.save()"
fi

exec "$@"
