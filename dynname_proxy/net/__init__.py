from .nics import get_ips as nics_get_ips
from .echoip import get_ips as echoip_get_ips


_get_ips = []
_get_ips.append(nics_get_ips)
_get_ips.append(echoip_get_ips)


def get_ips():
    ips = []
    for _get_ips_elem in _get_ips:
        ips_elem = _get_ips_elem()
        if ips_elem is None:
            continue
        ips += list(ips_elem.items())
    return dict(ips)
