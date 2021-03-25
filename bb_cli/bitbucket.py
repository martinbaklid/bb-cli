import urllib.parse
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import requests


class BitbucetException(Exception):
    pass


class NoSuchProjectException(BitbucetException):
    pass


class NoSuchRepoException(BitbucetException):
    pass


class Bitbucket:
    _API_PATH = '/rest/api/1.0/'

    def __init__(self, host: str, username: str, token: str) -> None:
        self._host = host
        self._username = username
        self._token = token

    def get_repos(self, project: str) -> List[Dict[str, Any]]:
        try:
            return self._call_paged(f'/projects/{project}/repos')
        except requests.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                raise NoSuchProjectException
            else:
                raise BitbucetException

    def get_pull_requests(
        self,
        project: str,
        repo: str,
    ) -> List[Dict[str, Any]]:
        endpoint = f'/projects/{project}/repos/{repo}/pull-requests'
        try:
            return self._call_paged(endpoint)
        except requests.HTTPError as e:
            if e.response.status_code == requests.codes.not_found:
                raise NoSuchRepoException
            else:
                raise BitbucetException

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
        res = requests.get(
            _full_url,
            params=params,
            auth=self._auth,
        )
        res.raise_for_status()
        return res.json()

    @property
    def _api_url(self) -> str:
        host = self._host
        if not host.startswith('http'):
            host = urllib.parse.urljoin('https://', f'//{self._host}')
        return urllib.parse.urljoin(host, self._API_PATH)

    @property
    def _auth(self) -> Tuple[str, str]:
        return (self._username, self._token)
