#!/bin/bash
#
# It builds and uploads the project image into the Google Container Registry.
#
# Usage: upload-docker-image.sh -p project-name -v version
#        deploy-app.sh -p dotted-ranger-333333 -v v2018-05
#

DIRECTORY=`dirname $0`

PROJECT_NAME={{ project_name | lower }}
VERSION=

while :; do
    case $1 in
        -p|--project-name) PROJECT_NAME=$2
        ;;
        -v|--version) VERSION=$2
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

gcloud config set project $PROJECT_NAME

# Generate the docker image

docker build -t gcr.io/preseries.com/$PROJECT_NAME:$VERSION ../

docker images | grep $PROJECT_NAME

# Upload the container image

gcloud auth configure-docker

docker push gcr.io/preseries.com/$PROJECT_NAME:$VERSION