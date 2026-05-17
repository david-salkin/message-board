#!/bin/bash
set -e

IMAGE_NAME="messageboard-app"
TAG="latest"

echo "🧪 Generating dynamic key and launching integration test suit..."
TEST_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Run container as a temporary process, dropping directly into pytest execution
docker run --rm \
    -e SECRET_KEY="${TEST_SECRET}" \
    -e DATABASE_URL="sqlite+aiosqlite:///:memory:" \
    "${IMAGE_NAME}:${TAG}" pytest -v
