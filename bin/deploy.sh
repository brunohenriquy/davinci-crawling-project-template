#!/bin/bash
#
# Usage: deploy-app.sh [-p project-name] [-v version] [--promote yes] [--optimized yes] [--r gcr.io] app.yaml
#        deploy-app.sh -v v2019-09 --promote yes --optimized yes --r gcr.io custom-flex-app.yaml
#

DIRECTORY="$( cd "$(dirname "$0")" ; pwd -P )"

# Sandbox
DOCKER_REPO="gcr.io"
PROJECT_NAME=
CODE_PROJECT_NAME={{ project_name | lower }}
CODE_PROJECT_VERSION=
GAE_VERSION=
NO_PROMOTE="--no-promote"
OPTIMIZED="--build-arg optimized=no"
YAML_FILE=

while :; do
    case $1 in
        -p|--project) PROJECT_NAME=$2
        ;;
        -v|--version)
            GAE_VERSION=$2
            CODE_PROJECT_VERSION="-v $2"
        ;;
        -r|--docker-repo) DOCKER_REPO=$2
        ;;
        --promote) NO_PROMOTE=""
        ;;
        --optimized) OPTIMIZED="--build-arg optimized=yes"
        ;;
        *)  YAML_FILE=$1
            shift
            break
    esac
    shift 2
done

if [ -z "$PROJECT_NAME" ]
then
      echo "The project-name must be specified"
      exit 2
fi

if [ -z "$YAML_FILE" ]
then
      echo "The YAML file must be specified"
      exit 2
fi

export DOCKER_IMAGE="${DOCKER_REPO}/${PROJECT_NAME}/${CODE_PROJECT_NAME}:${GAE_VERSION}"

echo "Project: ${PROJECT_NAME}"
echo "Code Project: ${CODE_PROJECT_NAME}"
echo "Code Version: ${CODE_PROJECT_VERSION}"
echo "GAE Version: ${GAE_VERSION}"
echo "Bucket: gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}"
echo "Docker image: ${DOCKER_IMAGE}"

gcloud config set project $PROJECT_NAME

cd $DIRECTORY/..

# The generation of the image takes to long and a DEADLINE_EXCEED happens
# with the default timeout.

gcloud config set app/cloud_build_timeout 10000

# Prepare the GS bucket to upload the static files
gsutil mb gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}

# Set public access to the GS bucket
gsutil defacl set public-read gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}

# Configure the CORS to allow access to the resources from different origins
export GAE_VERSION=$GAE_VERSION
envsubst < $DIRECTORY/cors-json-file.json > $DIRECTORY/deploy.cors-json-file.json
gsutil cors set $DIRECTORY/deploy.cors-json-file.json gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}
gsutil cors get gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}

OLD_STATIC_URL=$STATIC_URL
OLD_COMPRESS_ENABLED=$COMPRESS_ENABLED
OLD_COMPRESS_OFFLINE=$COMPRESS_OFFLINE

export STATIC_URL="https://storage.googleapis.com/static-${CODE_PROJECT_NAME}-${GAE_VERSION}/static/"
export COMPRESS_ENABLED=True
export COMPRESS_OFFLINE=True

# Generate the locale message files
./compile_messages.sh
# Collect all the static files and copy them into the /static folder
python manage.py collectstatic --noinput
# Clean the old compressed files
rm -rf static/compressed
# Compress the files
python manage.py compress

STATIC_URL=$OLD_STATIC_URL
COMPRESS_ENABLED=$OLD_COMPRESS_ENABLED
COMPRESS_OFFLINE=$OLD_COMPRESS_OFFLINE

# Sync the GS bucket with the changes in the static files
# (including the compressed files)
gsutil rsync -R static/ gs://static-${CODE_PROJECT_NAME}-${GAE_VERSION}/static

# Substitution of GITHUB env variables (GITHUB_USERNAME, GITHUB_PASSWORD)
envsubst < requirements.txt.template > requirements.txt

# Substitutions on the YAML file (for instance GAE_VERSION)
envsubst < $YAML_FILE > processed-${YAML_FILE}

# cp $GOOGLE_APPLICATION_CREDENTIALS ./credentials.json

# Build the docker image
# docker build -t $DOCKER_IMAGE .

# Upload image to Google
# gcloud docker -- push $DOCKER_IMAGE

# gcloud app deploy using the previous image and the processed flex-app.yaml (other available params: --log-http --verbosity=debug)
gcloud app deploy --project $PROJECT_NAME \
    --image-url $DOCKER_IMAGE \
    $CODE_PROJECT_VERSION $NO_PROMOTE processed-${YAML_FILE}
