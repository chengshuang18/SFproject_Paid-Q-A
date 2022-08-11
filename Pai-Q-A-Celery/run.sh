cd /var/lib/code/paid_q_a
ls
celery -A manage.my_celery worker -l info -P eventlet -c 10
