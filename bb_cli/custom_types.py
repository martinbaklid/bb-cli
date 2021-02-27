import urllib.parse


SPACE_SEP_LIST = lambda x: x.split()
HOST = lambda h: urllib.parse.urljoin("https://", h)
