from pathlib import Path

from click.testing import CliRunner

from bb_cli.main import main


def test__init():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    inputs = (
        'http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/repos',  # noqa: E501
        'olanormann',
        'a_long_token',
    )
    expected = (
        'Welcome to Bitbucket CLI',
        'Starting first time configuration',
        'Provide the url to your bitbucket server',
        '(eg. https://company.bitbucket-server.com):',
        'http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/repos',  # noqa: E501
        'Provide your username:',
        'olanormann',
        'BitBucket CLI needs a personal api token with read premisions.',
        '    1. Go to http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/plugins/servlet/access-tokens/manage',  # noqa: E501
        '    2. Click "Create a token"',
        '    3. Set "Token name" and select "Read Premisions"',
        '    4. Click create and copy the token',
        'Paste your token here:',
        'a_long_token',
        'Config initialized in ./config.yaml:',
        'To change configuration use "bb-cli config edit"',
        '',
    )
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['init'], input='\n'.join(inputs))
        assert result.stdout == '\n'.join(expected)


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
