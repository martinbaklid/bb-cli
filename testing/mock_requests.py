import json
import os
from typing import Any
from typing import Dict
from typing import Sequence
from typing import Tuple

import requests


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
        self.url = ''

    def json(self) -> Dict[str, Any]:
        return json.loads(self._body)

    @staticmethod
    def from_resource(resource_path):
        return FakeResponse(_get_resource(resource_path))

    def raise_for_status(self):  # copied from requests source
        """Raises :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = '{} Client Error: {} for url: {}'.format(
                self.status_code, '', self.url,
            )

        elif 500 <= self.status_code < 600:
            http_error_msg = '{} Server Error: {} for url: {}'.format(
                self.status_code, '', self.url,
            )

        if http_error_msg:
            raise requests.HTTPError(http_error_msg, response=self)


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
        response = url_mapping[key]
        response.url = url
        return response
    return get
