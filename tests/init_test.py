from click.testing import CliRunner

from bb_cli.init import init


def test__init():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    inputs = (
        'http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/repos',  # noqa: E501
        'olanormann',
        'a_long_token',
        'no',
        '/project_path',
        'web samp',
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
        'Do you want your personal repos managed (yes/no) [yes]:',
        'no',
        'Where do you want the Bitbucket projects cloned [~/projects]:',
        '/project_path',
        'List the slugs of projects you want manage',
        '(eg. "PROJ_SLUG1 PROJ_SLUG2"):',
        'web samp',
        'Config initialized in ./config.yaml:',
        'To change configuration use "bb-cli config edit"',
        '',
    )
    with runner.isolated_filesystem():
        result = runner.invoke(init, input='\n'.join(inputs))
        assert result.stdout == '\n'.join(expected)
