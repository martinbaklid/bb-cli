import os

from click.testing import CliRunner

import bb_cli.config
from bb_cli.config import Config
from bb_cli.main import main

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


def test__config_edit(mock_click_edit):
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    with runner.isolated_filesystem():
        os.environ['BB_CLI_APP_DIR'] = '.'
        bb_cli.config.dump(DUMMY_CONFIG)

        res = runner.invoke(main, ['config', 'edit'])

    assert res.exit_code == 0
    mock_click_edit.assert_called_once_with(filename='./config.yaml')


def test__config_edit_no_config():
    runner = CliRunner(env={'BB_CLI_APP_DIR': '.'})
    with runner.isolated_filesystem():

        res = runner.invoke(main, ['config', 'edit'])

    assert res.stdout == "Error: Can't find config file in ./config.yaml\n"
    assert res.exit_code == 1
