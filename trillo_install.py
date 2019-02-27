import fileinput
import subprocess
import argparse


def main():
  parser = argparse.ArgumentParser(
      description='certificates and start/stop/update containers')
  parser.add_argument(
      'action', choices=['certificates', 'start', 'stop', 'update'],
      help='action of certificate install and starting/stopping/updating '
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
  elif args.action == "certificates":
    _dict = {}
    for i in ["domain", "email"]:
      if getattr(args, i) is not None:
        _dict[i] = getattr(args, i)
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
    subprocess.call(["docker-compose", "down"])


if __name__ == "__main__":
  main()
