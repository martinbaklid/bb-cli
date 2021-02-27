from unittest import mock

import pytest
import requests


@pytest.fixture
def mock_requests_get():
    with mock.patch.object(requests, "get") as mck:
        yield mck
