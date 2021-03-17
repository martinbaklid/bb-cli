import builtins
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


@pytest.fixture
def mock_input():
    with mock.patch.object(builtins, 'input') as mck:
        def setup_inputs(*inputs):
            it = iter(inputs)

            def side_effect(s):
                print(s, end='')
                return next(it)
            mck.side_effect = side_effect
        yield setup_inputs
