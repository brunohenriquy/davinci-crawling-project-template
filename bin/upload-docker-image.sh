#!/bin/bash
#
# It builds and uploads the project image into the Google Container Registry.
#
# Usage: upload-docker-image.sh -p project-name -v version
#        deploy-app.sh -p dotted-ranger-333333 -v v2018-05
#

DIRECTORY=`dirname $0`

PROJECT_NAME=
CODE_PROJECT_NAME={{ project_name | lower }}
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
      echo "The project-name must be specified. Ex. -p dotted-ranger-333333"
      exit 2
fi

if [ -z "$VERSION" ]
then
      echo "The project version must be specified. Ex. -v v0.1.0"
      exit 2
fi

gcloud config set project $PROJECT_NAME

# Generate the docker image

docker build -t gcr.io/$PROJECT_NAME/$CODE_PROJECT_NAME:$VERSION ../

docker images | grep $CODE_PROJECT_NAME

# Upload the container image

gcloud auth configure-docker

docker push gcr.io/$PROJECT_NAME/$CODE_PROJECT_NAME:$VERSION