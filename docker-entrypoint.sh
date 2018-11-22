#!/bin/sh

# Prepare log files and start outputting logs to stdout
mkdir logs
touch logs/{{ project_name }}-gunicorn.log
touch logs/{{ project_name }}-access.log
tail -n 0 -f logs/*.log &

sed -e "s/\${DB_HOST}/$DB_HOST/" \
    -e "s/\${DB_PORT}/$DB_PORT/" \
    -e "s/\${DB_USER}/$DB_USER/" \
    -i conf/gae_pgbouncer.ini

sed -e "s/\${DB_USER}/$DB_USER/" \
    -e "s/\${DB_PASSWORD}/$DB_PASSWORD/" \
    -i conf/gae_pgbouncer_users.txt

# Start the pgbouncer pool in local
pgbouncer -d -u pgbouncer `pwd`/conf/gae_pgbouncer.ini

# Start Gunicorn processes
echo Starting Gunicorn.

# Start WSGI server
gunicorn --config {{ project_name }}/gunicorn.conf.py {{ project_name }}.wsgi -b :8000

# Wait 2 second until gunicorn has started all its workers
sleep 2

# Get the number of gunicorn processes started
WORKERS=`ps aux | grep gunicorn | wc -l`

echo "Starting Daphne Workers (${WORKERS})."
# Start Daphne WORKERS
for i in $(seq 0 $((WORKERS-2))); do python manage.py runworker --settings {{ project_name }}.settings channels & done

echo Starting Nginx server
# Start nginx
nginx -c `pwd`/conf/gae_prod_nginx.conf

echo Starting Daphne server
# Start Daphne
daphne sky.asgi:application -p 9000 -b 0.0.0.0
gunicorn -b :$PORT -c {{ project_name }}/gunicorn.conf.py {{ project_name }}.wsgi