#!/usr/bin/env bash

rtdsTag=${1:-3.0.296}
pubsubTag=${2:-3.0.273}

gcloud docker -- pull gcr.io/project-trillort/trillo-gke-tasker:${pubsubTag}
gcloud docker -- pull gcr.io/project-trillort/trillo-rt:${rtdsTag}
gcloud docker -- pull gcr.io/project-trillort/trillo-rt/trillo-data-service:${rtdsTag}