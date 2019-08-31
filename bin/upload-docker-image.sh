#!/bin/bash
#
# It builds and uploads the project image into the Google Container Registry.
#
# Usage: upload-docker-image.sh -p project-name -v version -o optimized? -r docker-repo
#        upload-docker-image.sh -p dotted-ranger-212213 -v v2018-05 -o yes -r eu.gcr.io
#

DIRECTORY=`dirname $0`

DOCKER_REPO="gcr.io"
PROJECT_NAME=
CODE_PROJECT_NAME={{ project_name | lower }}
OPTIMIZED="optimized=no"
VERSION=

while :; do
    case $1 in
        -p|--project-name) PROJECT_NAME=$2
        ;;
        -v|--version) VERSION=$2
        ;;
        -o|--optimized) OPTIMIZED="optimized=$2"
        ;;
        -r|--docker-repo) DOCKER_REPO=$2
        ;;
        *) break
    esac
    shift 2
done

if [ -z "$PROJECT_NAME" ]
then
      echo "The project-name must be specified. Ex. -p dotted-ranger-212213"
      exit 2
fi

if [ -z "$VERSION" ]
then
      echo "The project version must be specified. Ex. -v v0.1.0"
      exit 2
fi

gcloud config set project $PROJECT_NAME

# Generate the docker image

docker build --build-arg $OPTIMIZED \
    --build-arg gae_project_name=$PROJECT_NAME \
    --build-arg project_name=$CODE_PROJECT_NAME \
    --build-arg version=$VERSION \
    -t $DOCKER_REPO/$PROJECT_NAME/$CODE_PROJECT_NAME:$VERSION ../

docker images | grep $CODE_PROJECT_NAME

# Upload the container image

gcloud auth configure-docker

docker push $DOCKER_REPO/$PROJECT_NAME/$CODE_PROJECT_NAME:$VERSION