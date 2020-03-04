#!/usr/bin/env bash

COMPUTE_ENGINE_SA_EMAIL=$(gcloud iam service-accounts list --filter="name:Compute Engine default service account" --format "value(email)")
PROJECTID=`gcloud projects list | awk 'FNR>1 {print$1}'`

gcloud projects get-iam-policy ${PROJECTID}  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:${COMPUTE_ENGINE_SA_EMAIL}"
