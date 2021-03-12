import json
import os
from typing import Any
from typing import Dict
from typing import Sequence
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

    def __init__(self, body: str = ''):
        self._body = body

    def json(self) -> Dict[str, Any]:
        return json.loads(self._body)

    @staticmethod
    def from_resource(resource_path):
        return FakeResponse(_get_resource(resource_path))


def get_side_effect(url_mapping):
    def get(
        url: str,
        params: Dict[str, str],
        auth: Tuple[str, str],
    ) -> FakeResponse:
        key: Tuple[Sequence[str], ...] = (url,)
        if params:
            key = (
                *key,
                *((k, v) for k, v in params.items()),
            )
        return url_mapping[key]
    return get
