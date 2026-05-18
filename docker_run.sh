#!/bin/bash
set -e

IMAGE_NAME="messageboard-app"
TAG="latest"
CONTAINER_NAME="messageboard-prod"
PORT=8000

# 1. Clean up old container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🧹 Removing existing container: ${CONTAINER_NAME}..."
    docker rm -f ${CONTAINER_NAME}
fi

# 2. Dynamically generate a secure key using python (guaranteed cross-platform)
echo "🔐 Generating temporary runtime SECRET_KEY..."
RUNTIME_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

echo "🚀 Booting up container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}":8000 \
    -e PYTHONPATH=/app \
    -e SECRET_KEY="${RUNTIME_SECRET}" \
    -e ACCESS_TOKEN_EXPIRE_MINUTES=60 \
    -e DATABASE_URL="sqlite+aiosqlite:///app/database.db" \
    "${IMAGE_NAME}:${TAG}"

echo "📡 Container running at http://localhost:${PORT}"
echo "📝 Run 'docker logs -f ${CONTAINER_NAME}' to view runtime logs."
