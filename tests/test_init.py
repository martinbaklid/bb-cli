from click.testing import CliRunner
from bb_cli.init import init

test__init_input = """
http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/repos
olanormann
a_long_token
no
/project_path
web samp
""".strip()

test__init_expected_output = """
Welcome to Bitbucket CLI
Starting first time configuration
Provide the hostname (with protocol prefix) for your bitbucket server (eg. https://company.bitbucket-server.com): http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/repos
Provide your username: olanormann
To use BitBucket CLI you need to provide personal api token with read premisions.
    1. Go to http://fake.bitbucket-server.com/rest/api/1.0/projects/fake_proj/plugins/servlet/access-tokens/manage and click "Create a token"
    2. Set an appropriate "Token name" and give the token "Read Premisions"
    3. Click create and copy the token
Paste your token here: a_long_token
Do you want your personal repos managed (yes/no) [yes]: no
Where do you want the Bitbucket projects cloned [~/projects]: /project_path
List the project slugs of the projects you want manage (eg. "PROJ_SLUG1 PROJ_SLUG2"): web samp
Config initialized in ./config.yaml:
To change configuration use "bb-cli config edit"
""".lstrip()

def test__init():
    runner = CliRunner(env={ "BB_CLI_APP_DIR": "." })
    with runner.isolated_filesystem():
        result = runner.invoke(init, input=test__init_input)
        print(result.stdout)
        assert result.stdout == test__init_expected_output
