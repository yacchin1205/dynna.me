from datetime import datetime
import json
import hashlib
import hmac
import logging
import re
import requests


logger = logging.getLogger(__name__)


def get_proxy_ip(request):
    host = request.headers['host']
    m = re.match(r'^([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(\:[0-9]+)?$', host)
    if not m:
        return None
    return m.group(1)

class DynnameAPI:

    def __init__(self, config):
        self.config = config

    def update_proxy(self, proxy_ip=None, acme_validation=None):
        proxy_id = self.config['proxy_id'] if 'proxy_id' in self.config else None
        if proxy_id is None:
            payload = {
                'proxy_ip': proxy_ip,
                'name': self.config['name'] if 'name' in self.config else None,
                'secret': self.config['secret'],
            }
            if acme_validation is not None:
                payload['acme_validation'] = acme_validation
            data = json.dumps(payload).encode('utf8')
            url = 'https://dynna.me/api/v1/proxies/'
            headers = {
                'Content-Type': 'application/json',
            }
            resp = requests.put(url, headers=headers, data=data)
        else:
            payload = {
                'proxy_ip': proxy_ip,
                'name': self.config['name'] if 'name' in self.config else None,
            }
            if proxy_ip is not None:
                payload['proxy_ip'] = proxy_ip
            if acme_validation is not None:
                payload['acme_validation'] = acme_validation
            url = f'https://dynna.me/api/v1/proxies/{proxy_id}'
            data = json.dumps(payload).encode('utf8')
            hash = hashlib.sha256()
            hash.update(data)
            headers = {
                'Content-Type': 'application/json',
                'Host': 'dynna.me',
                'x-dynname-client-id': proxy_id,
                'x-dynname-epoch': str(int(datetime.now().timestamp() * 1000)),
                'x-dynname-content-sha256': hash.hexdigest(),
            }
            signature = self._compute_signature('POST', url, {}, headers, data)
            logger.debug('Signature: {}'.format(signature))
            headers['Authorization'] = signature
            resp = requests.post(url, headers=headers, data=data)
        resp.raise_for_status()
        proxy_settings = resp.json()
        if proxy_settings['status'] != 'ok':
            raise Exception(proxy_settings['status'])
        return proxy_settings['proxy_id'], proxy_settings['proxy_config_url']

    def get_proxy(self):
        proxy_id = self.config['proxy_id'] if 'proxy_id' in self.config else None
        if proxy_id is None:
            raise Exception('Proxy not defined')
        url = f'https://dynna.me/api/v1/proxies/{proxy_id}'
        data = b''
        hash = hashlib.sha256()
        hash.update(data)
        headers = {
            'Content-Type': 'application/json',
            'Host': 'dynna.me',
            'x-dynname-client-id': proxy_id,
            'x-dynname-epoch': str(int(datetime.now().timestamp() * 1000)),
            'x-dynname-content-sha256': hash.hexdigest(),
        }
        signature = self._compute_signature('GET', url, {}, headers, data)
        logger.debug('Signature: {}'.format(signature))
        headers['Authorization'] = signature
        resp = requests.get(url, headers=headers, data=data)
        resp.raise_for_status()
        proxy_settings = resp.json()
        if proxy_settings['status'] != 'ok':
            raise Exception(proxy_settings['status'])
        return proxy_settings

    def _compute_signature(self, method, url, queries, headers, data):
        secret = self.config['secret']
        # Canonical Request = HTTP Verb + '\n' +
        # Canonical URI + '\n' + Canonical Query String + '\n' +
        # Canonical Headers + '\n' + Signed Headers
        # StringToSign = 'NOTIFYG-HMAC-SHA256' + '\n' + EpochTime + '\n' +
        # Hex(SHA256Hash(Canonical Request))
        # SigningKey = Hex(HMAC-SHA256(Secret, 'NOTIFYG-202101'))
        # Signature = Hex(HMAC-SHA256(SigningKey, StringToSign))
        canonical_request = method + '\n' + url + '\n'
        querykeys = sorted(queries.keys())
        canonical_query_string = '&'.join(['{}={}'.format(requests.utils.quote(key),
                                                          requests.utils.quote(queries[key]))
                                           for key in querykeys])
        canonical_request += canonical_query_string + '\n'
        headercands = {'host', 'content-type', 'x-dynname-epoch', 'x-dynname-client-id', 'x-dynname-content-sha256'}
        headerkeys = sorted([k for k in headers.keys() if k.lower() in headercands],
                            key=lambda x: x.lower())
        canonical_headers = '\n'.join(['{}:{}'.format(key.lower(), headers[key].strip())
                                       for key in headerkeys])
        canonical_request += canonical_headers + '\n'
        canonical_request += ';'.join([k.lower() for k in headerkeys])
        logger.debug('CanonicalRequest: {}'.format(canonical_request))
        hash = hashlib.sha256()
        hash.update(canonical_request.encode('utf8'))
        string_to_sign = 'DYNNAME-HMAC-SHA256\n' + headers['x-dynname-epoch'] + '\n' + hash.hexdigest()
        logger.debug('StringToSign: {}'.format(string_to_sign))
        signing_key = hmac.new(secret.encode('utf8'), digestmod=hashlib.sha256)
        signing_key.update(b'DYNNAME-202111')
        logger.debug('SigningKey: {}'.format(signing_key.hexdigest()))
        signature = hmac.new(signing_key.hexdigest().encode('utf8'), digestmod=hashlib.sha256)
        signature.update(string_to_sign.encode('utf8'))
        return signature.hexdigest()
