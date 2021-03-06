#!/bin/bash

set -e

python manage.py wait_for_db
python manage.py db upgrade
python manage.py translate_compile

if [ "$NOI_ENVIRONMENT" == production ]; then
    python manage.py build_sass
    exec gunicorn wsgi:application -b 0.0.0.0:5000
else
    exec python develop.py
fi
