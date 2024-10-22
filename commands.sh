#!/bin/bash

# ./manage.py update_countries
# ./manage.py update_provinces
# ./manage.py update_cities
# ./manage.py update_geo_farsi

#./manage.py loaddata geo

# Recreate All Message
# run this for create file django.po after create, manule translate to persian :
# ./manage.py makemessages -l 'fa_IR' -i env

# after translate en to farsi in django.po then run this command :
# ./manage.py compilemessages


# python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'