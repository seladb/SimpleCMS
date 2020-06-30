#!/bin/bash

python manage.py migrate

python manage.py loaddata SimpleCmsAPI/fixtures/demo_data.json

python manage.py runserver 0.0.0.0:8000
