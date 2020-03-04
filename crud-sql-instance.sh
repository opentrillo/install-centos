#!/usr/bin/env bash

set -x

if [[ $# -ne 3 ]]; then
  echo "Error: missing arguments"
  exit 1
fi

crud=$1
dbInstance=$2
secret=$3

zone=$(gcloud --format="value(zone)" compute instances list --filter="name=($(hostname))")
publicIPAddress=$(gcloud --format="value(networkInterfaces[0].accessConfigs[0].natIP)" compute instances list --filter="name=($(hostname))")


if (( $crud == "1" )); then
  gcloud sql instances create ${dbInstance} --tier=db-g1-small --zone ${zone} --authorized-networks=${publicIPAddress}
  gcloud sql instances patch ${dbInstance} --backup-start-time 06:00
  gcloud sql users set-password root --host=% --instance ${dbInstance} --password ${secret}
  gcloud sql users set-password trillo --host=% --instance ${dbInstance} --password ${secret}
else
  gcloud sql instances patch ${dbInstance} --quiet --authorized-networks=${publicIPAddress}
fi


