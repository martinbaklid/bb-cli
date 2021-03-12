from unittest import mock

import pytest
import requests


@pytest.fixture
def mock_requests_get():
    with mock.patch.object(requests, 'get') as mck:
        yield mck


@pytest.fixture
def mock_load_config():
    with mock.patch('bb_cli.config.load') as mck:
        yield mck
