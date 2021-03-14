import os

import bb_cli.config
from bb_cli.config import Config
from testing import os_utils

DUMMY_CONFIG = Config(
    version=1,
    host='bitbucket.server.com',
    username='user',
    token='token',
)


def test__dumps_load(tmp_path):
    with os_utils.cwd(tmp_path):
        os.environ['BB_CLI_APP_DIR'] = '.'
        bb_cli.config.dump(DUMMY_CONFIG)
        assert bb_cli.config.load()['version'] == 1
