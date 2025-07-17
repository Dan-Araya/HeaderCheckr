import requests

def get_headers(url: str) -> dict:
    response = requests.get(url, timeout=10)
    return dict(response.headers)
