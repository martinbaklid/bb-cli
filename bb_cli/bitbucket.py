import urllib.parse
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import requests


class Bitbucket:
    _API_PATH = '/rest/api/1.0/'

    def __init__(self, host: str, username: str, token: str) -> None:
        self._host = host
        self._username = username
        self._token = token

    def get_repos(self, project: str) -> List[Dict[str, Any]]:
        return self._call_paged(f'/projects/{project}/repos')

    def get_pull_requests(
        self,
        project: str,
        repo: str,
    ) -> List[Dict[str, Any]]:
        endpoint = f'/projects/{project}/repos/{repo}/pull-requests'
        return self._call_paged(endpoint)

    def _call_paged(
        self,
        endpoint: str,
        params: Dict[str, str] = {},
    ) -> List[Dict[str, Any]]:
        values = []
        params_to_pass = params
        while True:
            res = self._call(endpoint, params_to_pass)
            values += res['values']
            if res['isLastPage']:
                return values
            params_to_pass = {**params, 'start': res['nextPageStart']}

    def _call(self, endpoint: str, params: Dict[str, str] = {}) -> Any:
        _norm_endpoint = endpoint.strip('/')
        _full_url = urllib.parse.urljoin(self._api_url, _norm_endpoint)
        return requests.get(
            _full_url,
            params=params,
            auth=self._auth,
        ).json()

    @property
    def _api_url(self) -> str:
        host = urllib.parse.urljoin('https://', self._host)
        return urllib.parse.urljoin(host, self._API_PATH)

    @property
    def _auth(self) -> Tuple[str, str]:
        return (self._username, self._token)
