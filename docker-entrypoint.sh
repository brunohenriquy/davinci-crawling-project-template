#!/bin/sh

# Prepare log files and start outputting logs to stdout
mkdir logs
touch logs/{{ project_name | lower }}-gunicorn.log
touch logs/{{ project_name | lower }}-access.log
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

# Start WSGI server
gunicorn -b :$PORT -c {{ project_name | lower }}/gunicorn.conf.py {{ project_name | lower }}.wsgi