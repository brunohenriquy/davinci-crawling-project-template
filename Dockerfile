FROM gcr.io/google-appengine/python
LABEL name="davinci-crawling-{{ project_name | lower }}" \
      crawling_vendor="BuildGroup Data Services, Inc." \
      maintainer="Javier Alperte <xalperte@buildgroupai.com>" \
      # We need the Python 3.6 environment \
      python_version=python3.6 \
      description="DaVinci Crawling project {{ project_name | capfirst }} \
        in a container ready to be deployed on Google Cloud App."

# Project details
ARG docker_repo="eu.gcr.io"
ARG gae_project_name
ARG project_name="crawler_one"
ARG version="0.1.1"

LABEL version="${version}"

# Build using optimized flag to avoid compile the dse driver
# Ex. docker build --build-arg  optimized=yes
ARG optimized

# Version of Google Chrome Headless and Chromium Driver
# deb https://dl.google.com/linux/chrome/deb/ stable main
# apt-cache policy google-chrome-stable
ARG google_chrome="76.0.3809.132-1"
# https://chromedriver.chromium.org/downloads
ARG chromedriver="76.0.3809.126"

# Version of PhanthomJS
ARG phantomjs="2.1.1-linux-x86_64"

ENV SECRET_KEY "secret-key"

ENV STATIC_URL "/static/"

ENV DEBUG "False"

ENV DSE_SUPPORT "True"

ENV THROTTLE_ENABLED "True"

ENV SECURE_SSL_HOST ""
ENV SECURE_SSL_REDIRECT "True"

ENV GOOGLE_ANALYTICS_ID ""

ENV DB_HOST "127.0.0.1"
ENV DB_PORT 5432
ENV DB_NAME "{{ project_name | lower }}"
ENV DB_USER "{{ project_name | lower }}"
ENV DB_PASSWORD "{{ project_name | lower }}"

ENV CASSANDRA_DB_HOST "127.0.0.1,127.0.0.2,127.0.0.3"
ENV CASSANDRA_DB_NAME "{{ project_name | lower }}"
ENV CASSANDRA_DB_USER "cassandra"
ENV CASSANDRA_DB_PASSWORD "{{ project_name | lower }}"
ENV CASSANDRA_DB_STRATEGY "NetworkTopologyStrategy"
ENV CASSANDRA_DB_REPLICATION "3"

ENV HAYSTACK_ACTIVE "True"
ENV HAYSTACK_KEYSPACE "{{ project_name | lower }}"
ENV HAYSTACK_URL "http://127.0.0.1:8983/solr"
ENV HAYSTACK_ADMIN_URL "http://127.0.0.1:8983/solr/admin/cores"

ENV REDIS_HOST_PRIMARY=localshot
ENV REDIS_PORT_PRIMARY "6379"
ENV REDIS_PASS_PRIMARY ""

ENV EMAIL_HOST_USER "user"
ENV EMAIL_HOST_PASSWORD "password"

ENV PROJECT_DOCKER_IMAGE "eu.gcr.io/dotted-ranger-212213/{{ project_name | lower }}:v0-1-1"


# Install Nginx. It will serve all the incomming requests
RUN apt-get update && apt-get install -yq \
    nginx

# Copy the nginx configuration file. This sets up the behavior of nginx, most
# importantly, it ensure nginx listens on port 8080. Google App Engine expects
# the runtime to respond to HTTP requests at port 8080.
# COPY conf/gae_prod_nginx.conf /etc/nginx/nginx.conf

# create log dir configured in nginx.conf
RUN mkdir -p /var/log/{{ project_name | lower }}

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
RUN virtualenv --no-download /env -p /opt/python3.6/bin/python3.6

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Update the pip
RUN pip install --upgrade pip

# Add unstable repo to allow us to access latest GDAL builds
RUN echo deb http://ftp.uk.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update

# Install GDAL dependencies
RUN apt-get -t unstable install -y --allow-unauthenticated libgdal-dev g++

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.base.txt /app/requirements.base.txt
RUN if [ "x$optimized" = "yes" ] ; then CASS_DRIVER_NO_CYTHON=0 pip install -r /app/requirements.base.txt ; else CASS_DRIVER_NO_CYTHON=1 pip install -r /app/requirements.base.txt ; fi

ADD requirements.txt /app/requirements.txt
RUN if [ "x$optimized" = "yes" ] ; then CASS_DRIVER_NO_CYTHON=0 pip install -r /app/requirements.txt ; else CASS_DRIVER_NO_CYTHON=1 pip install -r /app/requirements.txt ; fi

# Install PhantomJS runtime dependencies
# https://hub.docker.com/r/wernight/phantomjs/
RUN apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
        ca-certificates \
        bzip2 \
        libfontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install PhantomJS official dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
        curl \
    && mkdir /tmp/phantomjs \
    && curl -L https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$phantomjs.tar.bz2 \
           | tar -xj --strip-components=1 -C /tmp/phantomjs \
    && cd /tmp/phantomjs \
    && mv bin/phantomjs /usr/local/bin \
    && cd \
    && apt-get purge --auto-remove -y \
        curl \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/*

# Install Chrome Headless
# Ex. https://github.com/justinribeiro/dockerfiles/blob/master/chrome-headless/Dockerfile

# Install deps + add Chrome Stable + purge all the things
RUN apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
	    apt-transport-https \
	    ca-certificates \
	    curl \
	    gnupg \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
	&& apt-get update && apt-get install -y --allow-unauthenticated \
	    google-chrome-stable=$google_chrome \
	    fontconfig \
	    fonts-ipafont-gothic \
	    fonts-wqy-zenhei \
	    fonts-thai-tlwg \
	    fonts-kacst \
	    fonts-symbola \
	    fonts-noto \
	    ttf-freefont \
	    --no-install-recommends \
    && apt-get purge --auto-remove -y curl gnupg \
	&& rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated \
        curl unzip \
    && mkdir /tmp/chromiumdriver \
    && curl -L https://chromedriver.storage.googleapis.com/$chromedriver/chromedriver_linux64.zip --output /tmp/chromiumdriver/chromedriver.zip \
    && unzip /tmp/chromiumdriver/chromedriver.zip -d /tmp/chromiumdriver \
    && rm /tmp/chromiumdriver/chromedriver.zip \
    && mv /tmp/chromiumdriver/chromedriver /usr/local/bin \
    && apt-get purge --auto-remove -y \
        curl unzip \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/*

# Add Chrome as a user
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome \
		&& mkdir -p /opt/google/chrome && chown -R chrome:chrome /opt/google/chrome

# Add the application source code.
ADD . /app

# Add the service account file to the container
ADD $GOOGLE_APPLICATION_CREDENTIALS /app/credentials.json

# Install Cloud-SQL-Proxy
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /app/cloud_sql_proxy \
    && chmod +x /app/cloud_sql_proxy \
    && mkdir /cloudsql; chmod 777 /cloudsql

# Run all the services
CMD ./docker-entrypoint.sh