#!/usr/bin/env bash

# Instructions for CentOS 7
# install docker and docker compose

sudo yum install -y nano telnet git bind-utils
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce
sudo usermod -aG docker $(whoami)
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo yum -y install epel-release
sudo yum -y install -y python-pip
sudo pip install docker-compose
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
#sudo yum -y install python36u
#sudo yum -y install python36u-pip
#sudo yum -y install python36u-devel
#sudo yum -y upgrade python*
sudo yum -y install htop
#sudo yum -y install nginx
#sudo systemctl start nginx
#sudo firewall-cmd --permanent --zone=public --add-service=http
#sudo firewall-cmd --permanent --zone=public --add-service=https
#sudo firewall-cmd --reload
#sudo systemctl enable nginx
sudo yum -y install git
sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt

# cd /opt/letsencrypt
# ./certbot-auto --nginx -d example.com -d www.example.com

#sudo ln -s /bin/python3.6 /usr/local/bin/python3

sudo git clone https://github.com/opentrillo/install-centos.git /etc/trillo
