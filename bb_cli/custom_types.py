import urllib.parse
from typing import List


def SPACE_SEP_LIST(x: str) -> List[str]: return x.split()
def HOST(h: str) -> str: return urllib.parse.urljoin('https://', h)
