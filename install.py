#! /usr/local/bin/python3

import fileinput
import re
import subprocess

import argparse
import time


def main():
  parser = argparse.ArgumentParser(
      description='install certificates and start/stop/update containers')
  parser.add_argument(
      'action', choices=['install-cert', 'start', 'stop', 'update'],
      help='actions for certificate install and starting/stopping/updating '
           'containers')
  parser.add_argument(
      '--domain', required=False, help='Fully qualified '
                                       'domain name')
  parser.add_argument(
      '--email', required=False, help='Email for LetsEncrypt')
  parser.add_argument(
      '--rt', required=False, help='trillo-rt version')
  parser.add_argument(
      '--ds', required=False, help='trillo-data-service version')
  parser.add_argument(
      '--simple', required=False, help='use docker-compose-simple')
  args = parser.parse_args()

  if args.action == "":
    parser.print_help()
  elif args.action == "install-cert":
    _dict = {}
    for i in ["domain", "email"]:
      if getattr(args, i) is not None:
        _dict[i] = getattr(args, i)
      else:
        parser.print_help()
        exit(1)

    print(args.action, _dict)

    subprocess.call(["docker-compose", "down"])
    for line in fileinput.input(['init-letsencrypt.sh'], inplace=True):
      print(line.replace('gcp.trillo.io', _dict['domain']), end='')
    for line in fileinput.input(['init-letsencrypt.sh'], inplace=True):
      print(line.replace('info@trillo.io', _dict['email']), end='')
    for line in fileinput.input(['./data/nginx/app.conf'], inplace=True):
      print(line.replace('gcp.trillo.io', _dict['domain']), end='')
    subprocess.check_call(["./init-letsencrypt.sh"])
    for line in fileinput.input(['./data/nginx/app.conf'], inplace=True):
      print(line.replace('www.trillo.io', 'trillo-rt:8020'), end='')
    time.sleep(5)
    subprocess.call(["docker-compose", "down"])
    time.sleep(1)
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "up", "-d"])
  elif args.action == "update":
    _dict = {}
    for i in ["rt", "ds"]:
      if getattr(args, i) is not None:
        _dict[i] = getattr(args, i)
      else:
        parser.print_help()
        exit(1)

    r = re.compile(r"_\d+$")
    for line in fileinput.input(['docker-compose.yml'], inplace=True):
      if 'trillo/trillo-rt' in line:
        print(r.sub("_%s" % _dict['rt'], line), end='')
      elif 'trillo/trillo-data-service' in line:
        print(r.sub("_%s" % _dict['ds'], line), end='')
      else:
        print(line, end='')

    subprocess.call(["docker-compose", "down"])
    time.sleep(1)
    subprocess.call(["docker-compose", "-f", "docker-compose.yml", "up", "-d"])

  elif args.action == "start":
    _simple = False
    if getattr(args, "simple") is not None:
      _simple = True
    if _simple:
      subprocess.call(["docker-compose", "down"])
      subprocess.call(
          ["docker", "login"])
      subprocess.call(
          ["docker-compose", "-f", "docker-compose-simple.yml", "up", "-d"])
    else:
      subprocess.call(["docker-compose", "down"])
      time.sleep(1)
      subprocess.call(["docker-compose", "-f", "docker-compose.yml", "up", "-d"])

  elif args.action == "stop":
    subprocess.call(["docker-compose", "down"])


if __name__ == "__main__":
  main()
