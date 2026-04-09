#!/bin/bash
set -e
pip install -r requirements.txt
cd icard
python manage.py collectstatic --noinput
python manage.py migrate