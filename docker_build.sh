#!/bin/bash
# Stop script on any error
set -e

IMAGE_NAME="messageboard-app"
TAG="latest"

echo "⚙️  Starting Docker Build..."

# Build the container cleanly, removing intermediate containers
docker build \
    --no-cache \
    -t "${IMAGE_NAME}:${TAG}" .

echo "✅ Image '${IMAGE_NAME}:${TAG}' built successfully."
