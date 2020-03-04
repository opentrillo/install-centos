#! /usr/bin/python3
import fileinput
import logging
import os
import random
import socket
import string
import time
from os import path
from subprocess import call, check_output, CalledProcessError, STDOUT, check_call

import requests

UPDATE_SQL = "0"

CREATE_SQL = "1"

TRILLO_SQL_NAME = "trillo-mysql"

DB_SECRET_TXT = "/gcs/system/db-secret.txt"

TRILLO_APPS_DOMAIN = 'trilloapps.com'
OPT_TRILLO = "/opt/trillo"

logger = logging.getLogger('root')
FORMAT = "[%(lineno)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def randomString(stringLength=10):
  """Generate a random string of fixed length """
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))


def main():
  logger.info("%s", "inside the trillo installer")

  # make sure that you are in correct folder
  os.chdir(OPT_TRILLO)

  # if already installed then docker-compose up
  if path.exists("./install-complete"):
    logger.info("application is already installed. proceeding to start")
    call("./mount-gcs-bucket.sh", shell=True)
    call("/gcs/system/mount-all-folders.sh", shell=True)
    call("docker-compose up -d", shell=True)
    exit(0)

  # enable services
  call("./enable-services.sh", shell=True)

  # reject if service account does not have roles
  try:
    roles = check_output("./get-service-account-roles.sh", stderr=STDOUT).decode()
    if roles.find("roles/owner") == -1:
      logger.info(roles)
      logger.info("The default service account cannot install the software.")
      exit(1)

  except CalledProcessError as e:
    logger.info(e.output.decode())
    exit(1)

  logger.info("Proceeding to install the software")

  # create ssh keys and move the auth key to /root/.ssh/authorized_keys
  call("./generate-key.sh", cwd="./secrets/ssh", shell=True)
  call("cat ./trillo-ssh.pub >> /root/.ssh/authorized_keys", cwd="./secrets/ssh", shell=True)

  # download new google secrets
  call("./svc-acc-key.sh", cwd="./secrets/google", shell=True)

  # set the bucket and server name
  gcs_bucket_name = None
  public_ip_address = None

  try:
    gcs_bucket_name = check_output("./get-bucket-name.sh", stderr=STDOUT).decode().strip()
    public_ip_address = check_output("./get-public-ip.sh", stderr=STDOUT).decode().strip()
  except CalledProcessError as e:
    logger.info(e.output.decode())
    exit(1)

  logger.info(gcs_bucket_name)
  logger.info(public_ip_address)

  server_name = 'apps-' + public_ip_address.replace(".", "-")
  server_fqdn_name = server_name + "." + TRILLO_APPS_DOMAIN
  logger.info("server fqdn: " + server_fqdn_name)

  # create DNS A record
  logger.info("Creating DNS record")
  call("./create-dns-record.sh " + server_fqdn_name + " " + public_ip_address, shell=True)

  # run the bucket creation script
  for line in fileinput.input(['./bucket/cors.json'], inplace=True):
    print(line.replace("__server_fqdn_name__", server_fqdn_name), end='')
  call("./create-bucket.sh", cwd="./bucket", shell=True)
  call("./copy-global-contents.sh", cwd="./bucket", shell=True)

  # mount gcs locally
  if not path.exists("/gcs/system"):
    call("./create-mount-gcs.sh", shell=True)

  logger.info("Provisioning MYSQL database")
  if path.exists(DB_SECRET_TXT):
    logger.info("Reading db secret from " + DB_SECRET_TXT)
    f = open(DB_SECRET_TXT, 'r')
    db_secret = f.readline().strip()
    f.close()
  else:
    logger.info("Creating a new db secret")
    db_secret = randomString()
    call("echo " + db_secret + " > " + DB_SECRET_TXT, shell=True)

  logger.info("db_secret: " + db_secret)

  # create mysql instance
  try:
    sql_instance = check_output("gcloud sql instances list", stderr=STDOUT, shell=True).decode().strip()
    logger.info("The list of SQL instances: " + sql_instance)
    if sql_instance.find(TRILLO_SQL_NAME) == -1:
      logger.info("MYSQL server is already created, grabbing its ip address and updating the white listing")
      call("./crud-sql-instance.sh" + " " + CREATE_SQL + " " + TRILLO_SQL_NAME + " " + db_secret, shell=True)
    else:
      call("./crud-sql-instance.sh" + " " + UPDATE_SQL + " " + TRILLO_SQL_NAME + " " + db_secret, shell=True)
  except CalledProcessError as e:
    logger.info(e.output.decode())
    exit(1)

  sql_server = check_output("./get-sql-address.sh " + TRILLO_SQL_NAME, stderr=STDOUT, shell=True).decode().strip()
  logger.info("MYSQL server IP address: " + sql_server)

  # modify docker-compose.yml
  for line in fileinput.input(['docker-compose.yml'], inplace=True):
    line = line.replace("__gcp_bucket_name__", gcs_bucket_name.strip())
    line = line.replace("__db_secret__", db_secret)
    line = line.replace("__sql_server__", sql_server)
    line = line.replace("__gcs_file_server__", socket.gethostname())
    line = line.replace("__server_fqdn_name__", server_fqdn_name)
    print(line, end='')

  for line in fileinput.input(['./data/nginx/app.conf'], inplace=True):
    print(line.replace('__server_fqdn_name__', server_fqdn_name), end='')

  check_call(["./init-letsencrypt.sh", server_fqdn_name])
  time.sleep(5)
  call(["docker-compose", "down"])

  logger.info("final update to the nginx config")
  for line in fileinput.input(['./data/nginx/app.conf'], inplace=True):
    print(line.replace('www.trillo.io', 'trillo-rt:8020'), end='')

  time.sleep(2)

  call(["docker-compose", "up", "-d"])
  call("touch ./install-complete", shell=True)

  while True:
    url = 'https://%s/' % server_fqdn_name
    response = requests.get(url)
    if response.status_code == 200:
      logger.info("Congratulations! The server is running at " + url)
      break
    time.sleep(10)
    logger.info("Checking if server is online")


if __name__ == "__main__":
  main()
