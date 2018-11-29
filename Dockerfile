FROM gcr.io/google-appengine/python

# We need the Python 3.6 environment
LABEL python_version=python3.6

ENV SECRET_KEY "secret-key"

ENV STATIC_URL "/static/"

ENV DEBUG "False"

ENV THROTTLE_ENABLED "True"

ENV COMPRESS_ENABLED "True"
ENV COMPRESS_OFFLINE "True"

ENV SECURE_SSL_REDIRECT "True"

ENV GOOGLE_ANALYTICS_ID ""

ENV DB_HOST "127.0.0.1"
ENV DB_PORT 3306
ENV DB_NAME "{{ project_name }}"
ENV DB_USER "{{ project_name }}"
ENV DB_PASS "{{ project_name }}"

ENV CASSANDRA_DB_HOST "127.0.0.1,127.0.0.2,127.0.0.3"
ENV CASSANDRA_DB_NAME "{{ project_name }}"
ENV CASSANDRA_DB_USER "{{ project_name }}"
ENV CASSANDRA_DB_PASSWORD "{{ project_name }}"
ENV CASSANDRA_DB_STRATEGY "NetworkTopologyStrategy"
ENV CASSANDRA_DB_REPLICATION "3"

ENV HAYSTACK_ACTIVE "True"
ENV HAYSTACK_KEYSPACE "{{ project_name }}"
ENV HAYSTACK_URL "http://127.0.0.1:8983/solr"
ENV HAYSTACK_ADMIN_URL "http://127.0.0.1:8983/solr/admin/cores"

ENV REDIS_HOST_PRIMARY=localshot
ENV REDIS_PORT_PRIMARY "6379"
ENV REDIS_PASS_PRIMARY ""

ENV EMAIL_HOST_USER "user"
ENV EMAIL_HOST_PASSWORD "password"


# Install Nginx. It will serve all the incomming requests
RUN apt-get update && apt-get install -yq \
    nginx

# Copy the nginx configuration file. This sets up the behavior of nginx, most
# importantly, it ensure nginx listens on port 8080. Google App Engine expects
# the runtime to respond to HTTP requests at port 8080.
COPY conf/gae_prod_nginx.conf /etc/nginx/nginx.conf

# create log dir configured in nginx.conf
RUN mkdir -p /var/log/{{ project_name }}

# Create a simple file to handle heath checks. Health checking can be disabled
# in app.yaml, but is highly recommended. Google App Engine will send an HTTP
# request to /_ah/health and any 2xx or 404 response is considered healthy.
# Because 404 responses are considered healthy, this could actually be left
# out as nginx will return 404 if the file isn't found. However, it is better
# to be explicit.
RUN mkdir -p /usr/share/nginx/www/_ah && \
    echo "healthy" > /usr/share/nginx/www/_ah/health

# Install PGBouncer library to manage a connection pool with CloudSQL
RUN apt-get update && apt-get install -yq \
    pgbouncer && \
    useradd pgbouncer && \
    mkdir /var/log/pgbouncer && \
    mkdir /var/run/pgbouncer && \
    chown pgbouncer:staff -R /var/log/pgbouncer && \
    chown pgbouncer:staff -R /var/run/pgbouncer

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv --no-download /env -p python3.6

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app

# Run all the services
CMD ./docker-entrypoint.sh