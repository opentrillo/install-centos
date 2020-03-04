#!/usr/bin/env bash

PROJECTID=`gcloud projects list | awk 'FNR>1 {print$1}'`
echo $PROJECTID

BUCKET_NAME=trillo-${PROJECTID}
TOPIC_NAME=trillo-gcs-topic
SUBSCRIPTION_NAME=trillo-gcs-sub

if gsutil mb gs://${BUCKET_NAME}/ ; then
  gsutil versioning set on gs://${BUCKET_NAME}/
  gsutil cp -r ./bucket-layout/groups gs://${BUCKET_NAME}/
  gsutil cp -r ./bucket-layout/users gs://${BUCKET_NAME}/
  gsutil cors set ./cors.json gs://${BUCKET_NAME}

  gcloud pubsub topics create ${TOPIC_NAME}
  gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC_NAME}
  gsutil notification create -t ${TOPIC_NAME} -f json gs://${BUCKET_NAME}
fi
