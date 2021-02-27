from typing import Dict
from unittest import mock
import json
import os


def _get_resource(resource_rel_path: str) -> str:
    with open(os.path.join("testing/resources/", resource_rel_path)) as f:
        return f.read()


def get_side_effect(url_resourcepath_mapping: str):
    def get(url, **_):
        return url_resourcepath_mapping[url]

    return get


class FakeResponse:
    """
    Simple Fake requests.Response implements a very limited subset of requests.Response API
    See https://github.com/psf/requests/blob/4f6c0187150af09d085c03096504934eb91c7a9e/requests/models.py#L589 for real implementation
    """

    def __init__(self, body: str = "", status_code: int = 200):
        self._body = body
        self.status_code = 200

    def json(self) -> Dict:
        return json.loads(self._body)

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    @staticmethod
    def from_resource_path(resource_path):
        return FakeResponse(_get_resource(resource_path))
