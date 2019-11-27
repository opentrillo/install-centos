#!/usr/bin/env bash

./trillort stop
docker rmi trillo/trillo-data-service:develop_latest
docker rmi trillo/trillo-rt:develop_latest
./trillort start
docker-compose logs -f
