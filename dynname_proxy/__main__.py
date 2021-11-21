import argparse
import logging
import sys
from .server import app
from .config import load_config, save_config


logger = logging.getLogger(__name__)


def modify_config(config_path, name=None):
    if name is None:
        return
    c = load_config(config_path)
    logger.debug(f'config: {c}')
    c['name'] = name
    save_config(config_path, c)

parser = argparse.ArgumentParser(description='Server for dynna.me')
parser.add_argument('-H', '--host', type=str, default='0.0.0.0',
                    help='Listen host')
parser.add_argument('-p', '--port', type=int, default=5000,
                    help='Listen port')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Debug mode')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Verbose mode')
parser.add_argument('-c', '--config', type=str, default='~/.dynname.json',
                    help='Dynname config')
parser.add_argument('--name', type=str, default=None,
                    help='Proxy name')

args = parser.parse_args(sys.argv[1:])

log_level = logging.DEBUG if args.verbose else logging.WARNING
LOG_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=log_level, format=LOG_FORMAT)

modify_config(args.config, name=args.name)
app.config['config_path'] = args.config

app.run(host=args.host, port=args.port, debug=args.debug)
