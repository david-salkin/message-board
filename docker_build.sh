#!/bin/bash
# Stop script on any error
set -e

IMAGE_NAME="messageboard-app"
TAG="latest"

echo "Starting Docker Build..."

# Remove intermediate containers
docker build \
	--no-cache \
	-t "${IMAGE_NAME}:${TAG}" .

echo "Image '${IMAGE_NAME}:${TAG}' built successfully."
