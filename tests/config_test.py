from click.testing import CliRunner

import bb_cli.config
from bb_cli.config import Config

DUMMY_CONFIG = Config(
    version=1,
    host='bitbucket.server.com',
    username='user',
    token='token',
)


def test__dumps_load():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    with runner.isolated_filesystem():
        bb_cli.config.dump(DUMMY_CONFIG)
        assert bb_cli.config.load()['version'] == 1
