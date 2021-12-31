import argparse
import json
import logging
import os
import sys
from ..server import DynnameAPI
from ..config import load_config
from ..net import get_ips


def _get_cert_path(cert_dir, fqdn):
    if fqdn.endswith('.'):
        fqdn = fqdn[:-1]
    path = os.path.join(cert_dir, fqdn)
    if not os.path.exists(path):
        return None
    return path


logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Command line tool for dynna.me')
parser.add_argument('-g', '--get', action='store_true',
                    help='Action: get proxy info')
parser.add_argument('-u', '--update', action='store_true',
                    help='Action: update proxy info')
parser.add_argument('--acme-validation', type=str, default=None,
                    help='ACME validation')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Debug mode')
parser.add_argument('--cert-dir', type=str, default=None,
                    help='Path to the certificate directory')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Verbose mode')
parser.add_argument('-c', '--config', type=str, default='~/.dynname.json',
                    help='Path of the dynname config')

args = parser.parse_args(sys.argv[1:])

log_level = logging.DEBUG if args.verbose else logging.WARNING
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=log_level, format=LOG_FORMAT)

config = load_config(args.config)
api = DynnameAPI(config)
if args.get:
    proxy = api.get_proxy() if 'proxy_id' in config else {}
    if args.cert_dir and 'fqdns' in proxy:
        proxy['cert_dirs'] = [_get_cert_path(args.cert_dir, fqdn) for fqdn in proxy['fqdns']]
    print(json.dumps(proxy))
elif args.update:
    proxy_ip = None
    if 'proxy_nic' in config and config['proxy_nic'] is not None:
        ips = get_ips()
        proxy_nic = config['proxy_nic']
        if proxy_nic in ips:
            proxy_ip = ips[proxy_nic]
        else:
            logger.warn(f'No nic: {proxy_nic}')
    if args.acme_validation is None and proxy_ip is None:
        logger.info('No properties to update')
        sys.exit(0)
    api.update_proxy(acme_validation=args.acme_validation, proxy_ip=proxy_ip)
else:
    print('Action not defined', file=sys.stderr)
    parser.print_help()
