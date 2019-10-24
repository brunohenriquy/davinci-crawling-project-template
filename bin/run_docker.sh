#!/bin/sh
#
# Usage: deploy-app.sh -p project-name -v version -i image
#        deploy-app.sh -p xxxxx -v v2018-09 -i gcr.io/buildgroupai.com/{{ project_name | lower }}:v2019-09
#

DIRECTORY="$( cd "$(dirname "$0")" ; pwd -P )"

# Sandbox
DOCKER_REPO="gcr.io"
PROJECT_NAME={{ project_name | lower }}
PROJECT_VERSION=
IMAGE_NAME="gcr.io/buildgroupai.com/{{ project_name | lower }}"

while :; do
    case $1 in
        -p|--project) PROJECT_NAME=$2
        ;;
        -v|--version) PROJECT_VERSION="$2"
        ;;
        -i|--image) IMAGE_NAME="$2"
        ;;
        *) break
    esac
    shift 2
done

if [ -z "$PROJECT_NAME" ]
then
      echo "The project-name must be specified"
      exit 2
fi

if [ -z "PROJECT_VERSION" ]
then
      echo "The version must be specified"
      exit 2
fi

source ../environment.sh

docker run -d --link=${PROJECT_NAME}-redis:redis --link=${PROJECT_NAME}-db:postgres \
    -p 8080:8080 \
    -e SECRET_KEY=$SECRET_KEY \
    -e STATIC_URL=$STATIC_URL \
    -e THROTTLE_ENABLED=$THROTTLE_ENABLED \
    -e DEBUG=$DEBUG \
    -e DSE_SUPPORT=$DSE_SUPPORT \
    -e GOOGLE_ANALYTICS_ID=$GOOGLE_ANALYTICS_ID \
    -e SECURE_SSL_HOST=$SECURE_SSL_HOST \
    -e SECURE_SSL_REDIRECT=$SECURE_SSL_REDIRECT \
    -e HAYSTACK_URL=$HAYSTACK_URL \
    -e HAYSTACK_ADMIN_URL=$HAYSTACK_ADMIN_URL \
    -e DB_HOST=$DB_HOST \
    -e DB_PORT=$DB_PORT \
    -e DB_NAME=$DB_NAME \
    -e DB_USER=$DB_USER \
    -e DB_PASSWORD=$DB_PASSWORD \
    -e CASSANDRA_DB_HOST=$CASSANDRA_DB_HOST \
    -e CASSANDRA_DB_NAME=$CASSANDRA_DB_NAME \
    -e CASSANDRA_DB_USER=$CASSANDRA_DB_USER \
    -e CASSANDRA_DB_PASSWORD=$CASSANDRA_DB_PASSWORD \
    -e CASSANDRA_DB_STRATEGY=$CASSANDRA_DB_STRATEGY \
    -e CASSANDRA_DB_REPLICATION=$CASSANDRA_DB_REPLICATION \
    -e CASSANDRA_DB_REPLICATION=$CASSANDRA_DB_REPLICATION \
    -e REDIS_HOST_PRIMARY=$REDIS_HOST_PRIMARY \
    -e REDIS_PORT_PRIMARY=$REDIS_PORT_PRIMARY \
    -e REDIS_PASS_PRIMARY=$REDIS_PASS_PRIMARY \
    -e EMAIL_HOST_USER=$EMAIL_HOST_USER \
    -e EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
    --name $PROJECT_NAME \
    $IMAGE_NAME
