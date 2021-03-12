import urllib.parse


def HOST(h: str) -> str: return urllib.parse.urljoin('https://', h)
