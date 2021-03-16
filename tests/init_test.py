import os
from pathlib import Path

import bb_cli.config
from bb_cli.init import init
from testing import os_utils


def test__init(tmp_path, capsys, mock_input):
    with os_utils.cwd(tmp_path):
        os.environ['BB_CLI_APP_DIR'] = '.'
        mock_input(
            'http://fake.bitbucket-server.com',
            'olanormann',
            'a_long_token',
        )

        return_code = init()

        config = bb_cli.config.load()
    out, _ = capsys.readouterr()
    assert return_code == 0
    assert out == (
        'Welcome to Bitbucket CLI\n'
        'Starting first time configuration\n'
        'Provide the url to your bitbucket server\n'
        '(eg. https://company.bitbucket-server.com):\n'
        'Provide your username:\n'
        'BitBucket CLI needs a personal api token with read premisions.\n'
        '    1. Go to '
        'http://fake.bitbucket-server.com/plugins/servlet/access-tokens/manage\n'  # noqa: E501
        '    2. Click "Create a token"\n'
        '    3. Set "Token name" and select "Read Premisions"\n'
        '    4. Click create and copy the token\n'
        'Paste your token here:\n'
        'Config initialized in ./config.yaml\n'
    )
    assert config['host'] == 'http://fake.bitbucket-server.com'
    assert config['username'] == 'olanormann'
    assert config['token'] == 'a_long_token'


def test__init_when_config_exits(tmp_path, capsys):
    with os_utils.cwd(tmp_path):
        os.environ['BB_CLI_APP_DIR'] = '.'
        Path('config.yaml').touch()

        return_code = init()

    _, err = capsys.readouterr()
    assert return_code == 1
    assert err == 'Error: Config already exists in ./config.yaml.\n'
