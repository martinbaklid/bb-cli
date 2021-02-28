import json
import os
from typing import Any
from typing import Callable
from typing import Dict
from typing import Tuple


def _get_resource(resource_rel_path: str) -> str:
    with open(os.path.join('testing/resources/', resource_rel_path)) as f:
        return f.read()


class FakeResponse:
    """
    Simple Fake requests.Response
    Implements a very limited subset of requests.Response API
    See https://github.com/psf/requests/blob/master/requests/models.py#L589
    for real implementation
    """

    def __init__(self, body: str = '', status_code: int = 200):
        self._body = body
        self.status_code = status_code

    def json(self) -> Dict[str, Any]:
        return json.loads(self._body)

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    @staticmethod
    def from_resource_path(resource_path):
        return FakeResponse(_get_resource(resource_path))


def get_side_effect(
    url_mapping: Dict[str, FakeResponse],
) -> Callable[[str, Tuple[str, str]], FakeResponse]:
    def get(url: str, auth: Tuple[str, str]) -> FakeResponse:
        return url_mapping[url]
    return get
