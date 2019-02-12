#!/usr/bin/env bash

docker build -t data-population-one-shot . -f docker/webserver/Dockerfile
docker run \
    --rm \
    --network host \
    --env-file mongodb_user_credentials.env \
    --env-file storage_credentials.env \
    -e PYTHONPATH=/app \
    --entrypoint="python3" \
    data-population-one-shot \
    aquascope/scripts/populate_system.py data/5p0xMAG_small
