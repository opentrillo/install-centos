#!/usr/bin/env bash

set -x

serverName=$1
ipAddress=$2
keyFile=./secrets/trillo/dns-record-creator.json

gcloud auth activate-service-account --key-file=${keyFile}

gcloud dns --project=project-trillort record-sets transaction start --zone=trilloapps-zone

gcloud dns --project=project-trillort record-sets transaction add ${ipAddress} --name=${serverName}. --ttl=300 --type=A --zone=trilloapps-zone

gcloud dns --project=project-trillort record-sets transaction execute --zone=trilloapps-zone

sleep 5

gcloud auth revoke trilloapps-dns-record-creator@project-trillort.iam.gserviceaccount.com

rm $keyFile