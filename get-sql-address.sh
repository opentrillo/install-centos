#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
  echo "Error: missing arguments"
  exit 1
fi

dbInstance=$1

echo $(gcloud sql instances describe ${dbInstance} --format='value(ipAddresses.ipAddress)')
