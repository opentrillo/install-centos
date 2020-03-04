#!/usr/bin/env bash


PROJECTID=`gcloud projects list | awk 'FNR>1 {print$1}'`
mount trillo-${PROJECTID}
