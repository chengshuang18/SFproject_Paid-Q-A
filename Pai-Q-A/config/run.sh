#!/bin/sh
rm -rf /var/lib/code/*
cp -r /opt/paid_q_a/ /var/lib/code/

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py insert_basic_param
python manage.py  runserver -h 0.0.0.0 -p 80
