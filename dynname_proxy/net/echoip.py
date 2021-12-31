import logging
import os
import re
import requests


logger = logging.getLogger(__name__)


def _get_echoip_servers():
    r = []
    for k, v in os.environ.items():
        m = re.match(r'^ECHOIP_(.+)$', k)
        if not m:
            continue
        r.append((m.group(1), v))
    return r

def get_ips():
    r = []
    for name, echoip_server in _get_echoip_servers():
        resp = requests.get(echoip_server, headers={'Accept': 'text/plain'})
        if resp.status_code != 200:
            logger.warn(f'echoip server {echoip_server} error: {resp.status_code}')
            continue
        addr = resp.text.strip()
        if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$', addr):
            logger.warn(f'echoip server {echoip_server} invalid text: {addr}')
            continue
        r.append((f'echoip.{name}', addr))
    return dict(r)
