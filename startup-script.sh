#!/bin/bash

if [ -f /sftp/startup-done ]; then
    echo "startup-done: skipping startup script!"
    exit 0
fi

snap remove google-cloud-sdk

# Create an environment variable for the correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get -qq  update && sudo apt-get -qq install google-cloud-sdk

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
apt-get -qq update
apt-get -qq install gcsfuse whois docker.io python-pip
pip install --upgrade docker-compose
groupadd sftpusers
sed --in-place '/sftp-server/d' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
tee -a /etc/ssh/sshd_config << END
Subsystem sftp internal-sftp
Match Group sftpusers
  PasswordAuthentication yes
  ChrootDirectory %h
  X11Forwarding no
  AllowTcpForwarding no
  ForceCommand internal-sftp
END
/etc/init.d/ssh restart
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
sudo bash install-logging-agent.sh
curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
sudo bash install-monitoring-agent.sh
mkdir /gcs
mkdir /sftp
touch /sftp/startup-done
