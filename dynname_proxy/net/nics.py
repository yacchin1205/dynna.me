import logging
import socket
try:
    import psutil
    psutil_not_found = False
except ImportError:
    psutil_not_found = True


logger = logging.getLogger(__name__)


def get_ips():
    if psutil_not_found:
        logger.warn('psutil not installed')
        return None
    r = []
    for name, nics in psutil.net_if_addrs().items():
        nics = [nic for nic in nics if nic.family == socket.AF_INET]
        for i, nic in enumerate(nics):
            r.append((f'psutil.{name}.{i}', nic.address))
    return dict(r)
