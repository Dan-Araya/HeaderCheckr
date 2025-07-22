import ipaddress
import socket
from urllib.parse import urlparse

def is_url_safe(url: str) -> bool:
    """
    Checks if a URL is safe for parsing.

    Returns False if:
    - It uses a scheme other than http/https
    - It points to a local, private, or reserved IP address
    - It cannot be resolved correctly

    Returns True only if the URL is safe to parse.
    """
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ('http', 'https'):
        return False

    hostname = parsed_url.hostname
    if hostname is None:
        return False

    else:
        ip = socket.gethostbyname(hostname)
        ip_objet = ipaddress.ip_address(ip)
        banned_ips = ("is_private",
        "is_loopback",
        "is_link_local",
        "is_reserved",
        "is_multicast",
        "is_unspecified")
        if any(getattr(ip_objet, attr) for attr in banned_ips):
            return False
        else:
            return True
