import requests

def get_headers(url: str) -> dict:
    #TODO add User-Agent": "Mozilla/5.0 (compatible; HeaderCheckr/1.0)"
    response = requests.get(url, timeout=10)
    return dict(response.headers)
