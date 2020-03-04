#!/usr/bin/env bash

PROJECTID=`gcloud projects list | awk 'FNR>1 {print$1}'`
echo $PROJECTID

BUCKET_NAME=trillo-${PROJECTID}

gsutil cp -r gs://trillo-public/fm/scripts/* gs://${BUCKET_NAME}/system



