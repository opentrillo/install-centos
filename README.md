# Installation of Trillo Runtime with Nginx and Let’s Encrypt

Before running any command make sure to "sudo su -". Also suggest
creating /etc/trillo for the following installation.

## Video Instructions
[![](http://img.youtube.com/vi/SRDPjArL1-k/0.jpg)](http://www.youtube.com/watch?v=SRDPjArL1-k "")

## Start Runtime
- ./trillort start-simple
- login into docker-hub account (account must be known to trillo.io)
- Once script is done, the runtime will be accessible at
  https://ip-address_or_hostname

## Stop Runtime
- ./trillort stop

## Update Runtime
- ./trillort update --rt 376 --ds 187

## Start Runtime with your registered domain and email
- ./trillort install-cert --domain your-host-FQDN --email <your_email>
- Follow the interactive install
- Once script is done, the runtime will be accessible at
  https://your-host-FQDN


## Debugging
Use 'docker-compose logs -f' to monitor logs

# Contributions
The nginx-certbot boilerplate code is based on
https://github.com/wmnnd/nginx-certbot

