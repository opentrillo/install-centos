#!/usr/bin/env bash

IP_ADDRESS=$(gcloud --format="value(networkInterfaces[0].accessConfigs[0].natIP)" compute instances list --filter="name=($(hostname))")
echo ${IP_ADDRESS}