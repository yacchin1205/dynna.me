import logging
from flask import Flask, request, redirect
from .service import get_proxy_ip, DynnameAPI
from .config import load_config, save_config
from .net import get_ips

app = Flask(__name__)
logger = logging.getLogger(__name__)


def _find_proxy_nic(proxy_ip):
    ips = get_ips()
    if ips is None:
        return None
    for k, v in ips.items():
        if v == proxy_ip:
            return k
    return None


@app.route("/.dynname/config")
def configure_proxy():
    proxy_ip = get_proxy_ip(request)
    if proxy_ip is None:
        host = request.headers['host']
        return f'You need to access the site by IP address: {host}', 400
    config = load_config(app.config['config_path'])
    api = DynnameAPI(config)
    proxy_id, proxy_config_url = api.update_proxy(proxy_ip=proxy_ip)
    config['proxy_id'] = proxy_id
    config['proxy_nic'] = _find_proxy_nic(proxy_ip)
    if config['proxy_nic'] is None:
        logger.info(f'No NICs: {proxy_ip}')
    save_config(app.config['config_path'], config)
    return redirect(proxy_config_url)
