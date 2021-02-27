from typing import Any, Dict, List
import requests
import urllib.parse


class Bitbucket:
    _API_PATH = "/rest/api/1.0/"

    def __init__(self, host: str, username: str, token: str) -> None:
        self._host = host
        self._username = username
        self._token = token

    def get_repos(self, project_slug: str) -> List[Dict[str, Any]]:
        values = []
        query = ""
        while True:
            res = self._call(f"/projects/{project_slug}/repos{query}")
            values += res["values"]
            if res["isLastPage"]:
                return values
            query = f"?start={res['nextPageStart']}"

    def _call(self, endpoint: str) -> Any:
        _norm_endpoint = endpoint.strip("/")
        _full_url = urllib.parse.urljoin(self._api_url, _norm_endpoint)
        return requests.get(_full_url, auth=(self._username, self._token)).json()

    @property
    def _api_url(self) -> str:
        host = urllib.parse.urljoin("https://", self._host)
        return urllib.parse.urljoin(host, self._API_PATH)
