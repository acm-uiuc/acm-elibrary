#!/bin/bash
source venv/bin/activate
cd application
python manage.py assets build
python manage.py runserver
