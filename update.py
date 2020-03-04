#! /usr/bin/python3
import fileinput
import json
import logging
import os
import time
from subprocess import call, check_output, CalledProcessError, STDOUT
import requests

TRILLO_APPS_DOMAIN = 'trilloapps.com'
OPT_TRILLO = "/opt/trillo"

logger = logging.getLogger('root')
FORMAT = "[%(lineno)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def main():
  logger.info("%s", "inside the trillo updater")

  # make sure that you are in correct folder
  os.chdir(OPT_TRILLO)

  public_ip_address = None

  try:
    public_ip_address = check_output("./get-public-ip.sh", stderr=STDOUT).decode().strip()
  except CalledProcessError as e:
    logger.info(e.output.decode())
    exit(1)

  logger.info(public_ip_address)

  server_name = 'apps-' + public_ip_address.replace(".", "-")
  server_fqdn_name = server_name + "." + TRILLO_APPS_DOMAIN
  logger.info("server fqdn: " + server_fqdn_name)

  # docker-compose down
  call(["docker-compose", "down"])

  # update scripts if there from public folder
  call("./copy-global-contents.sh", cwd="./bucket", shell=True)

  # read the released versions from public folder
  call("gsutil cp gs://trillo-public/fm/config.json .", shell=True)
  with open('./config.json') as f:
    config = json.load(f)

  logger.info(config)
  # pull the released versions
  call("./get-docker-images.sh " + config['rtdsTag'] + " " + config['pubsubTag'], shell=True)

  # update the docker-compose with latest versions
  dsServiceTagLine = '    image: gcr.io/project-trillort/trillo-rt/trillo-data-service:' + config['rtdsTag']
  taskerTagLine = '    image: gcr.io/project-trillort/trillo-gke-tasker:' + config['pubsubTag']
  rtServiceTagLine = '    image: gcr.io/project-trillort/trillo-rt:' + config['rtdsTag']

  for line in fileinput.input(['docker-compose.yml'], inplace=True):
    if 'gcr.io/project-trillort/trillo-rt/trillo-data-service:' in line:
      line = dsServiceTagLine
      # logger.info(dsServiceTagLine)
    elif 'gcr.io/project-trillort/trillo-gke-tasker:' in line:
      line = taskerTagLine
      # logger.info(taskerTagLine)
    elif 'gcr.io/project-trillort/trillo-rt:' in line:
      line = rtServiceTagLine
      # logger.info(rtServiceTagLine)
    print(line)

  # docker-compose up
  call(["docker-compose", "up", "-d"])

  # loop until system is ready
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
