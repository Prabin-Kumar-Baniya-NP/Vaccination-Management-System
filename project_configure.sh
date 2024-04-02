#!/bin/bash

# For creating the fake super user account
python manage.py populate_fake_superuser

# For creating the fake vaccine data
python manage.py populate_fake_vaccines

# For creating the fake center and storage data
python manage.py populate_fake_center

# For creating the fake campaign and slot data
python manage.py populate_fake_campaign

# Run the project using gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 2 mysite.wsgi:application
