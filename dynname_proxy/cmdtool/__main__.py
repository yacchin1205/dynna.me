import argparse
import json
import logging
import sys
from ..server import DynnameAPI
from ..config import load_config


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
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Verbose mode')
parser.add_argument('-c', '--config', type=str, default='~/.dynname.json',
                    help='Dynname config')

args = parser.parse_args(sys.argv[1:])

log_level = logging.DEBUG if args.verbose else logging.WARNING
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=log_level, format=LOG_FORMAT)

config = load_config(args.config)
api = DynnameAPI(config)
if args.get:
    proxy = api.get_proxy()
    print(json.dumps(proxy))
elif args.update:
    assert args.acme_validation is not None
    api.update_proxy(acme_validation=args.acme_validation)
else:
    print('Action not defined', file=sys.stderr)
    parser.print_help()
