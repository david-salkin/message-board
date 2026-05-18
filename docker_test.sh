#!/bin/bash
set -euo pipefail

IMAGE_NAME="messageboard-app"
TAG="latest"

echo "Building Docker test image..."
docker build --no-cache -t "${IMAGE_NAME}:${TAG}" .

echo "Generating dynamic key for test run..."
TEST_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

echo "Running tests inside container with local repository mounted and in-memory DB..."
docker run --rm \
    -v "$(pwd)":/app:rw \
    -w /app \
    -e PYTHONPATH=/app \
    -e SECRET_KEY="${TEST_SECRET}" \
    -e DATABASE_URL="sqlite+aiosqlite:///:memory:" \
    "${IMAGE_NAME}:${TAG}" \
    pytest -q tests/test_messageboard.py
