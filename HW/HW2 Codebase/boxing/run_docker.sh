#!/bin/bash

IMAGE_NAME="boxing-flask-app"
CONTAINER_TAG="latest"
HOST_PORT=5001
CONTAINER_PORT=5000
DB_VOLUME_PATH="./db"
BUILD=true
ENV_FILE=".env"
CONTAINER_NAME="${IMAGE_NAME}_container"

if [ "$BUILD" = true ]; then
  echo "Building Docker image..."
  docker build -t "${IMAGE_NAME}:${CONTAINER_TAG}" .
else
  echo "Skipping Docker image build..."
fi

if [ ! -d "${DB_VOLUME_PATH}" ]; then
  echo "Creating database directory at ${DB_VOLUME_PATH}..."
  mkdir -p "${DB_VOLUME_PATH}"
fi

if [ "$(docker ps -q -a -f name=${CONTAINER_NAME})" ]; then
  echo "Stopping running container: ${CONTAINER_NAME}"
  docker stop "${CONTAINER_NAME}"

  if [ $? -eq 0 ]; then
    echo "Removing container: ${CONTAINER_NAME}"
    docker rm "${CONTAINER_NAME}"
  else
    echo "Failed to stop container: ${CONTAINER_NAME}"
    exit 1
  fi
else
  echo "No running container named ${CONTAINER_NAME} found."
fi

echo "Running Docker container..."
docker run -d \
  --name "${CONTAINER_NAME}" \
  --env-file "${ENV_FILE}" \
  -v "$(pwd)/${DB_VOLUME_PATH}:/app/db" \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "${IMAGE_NAME}:${CONTAINER_TAG}"

echo "Docker container is running at http://localhost:${HOST_PORT}"
