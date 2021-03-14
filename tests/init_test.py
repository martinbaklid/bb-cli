from pathlib import Path

from click.testing import CliRunner

import bb_cli.config
from bb_cli.main import main


def test__init():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            ['init'],
            input=(
                'http://fake.bitbucket-server.com\n'
                'olanormann\n'
                'a_long_token\n'
            ),
        )
        config = bb_cli.config.load()

        assert result.stdout == (
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
            'Config initialized in ./config.yaml:\n'
            'To change configuration use "bb-cli config edit"\n'
        )
        assert config['host'] == 'http://fake.bitbucket-server.com'
        assert config['username'] == 'olanormann'
        assert config['token'] == 'a_long_token'


def test__init_when_config_exits():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    with runner.isolated_filesystem():
        Path('config.yaml').touch()

        result = runner.invoke(main, ['init'])

        assert result.stdout == (
            'Error: Config allready exsists in ./config.yaml. '
            'To change the configuration use '
            'bb-cli conifg edit\n'
        )
