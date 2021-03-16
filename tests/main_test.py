from unittest import mock

from bb_cli import main


def test__main_command_init():
    with mock.patch.object(main, 'init') as mck:
        main.main(('init',))

        mck.assert_called_once()


def test__main_command_pr_list():
    with mock.patch.object(main, 'list_all') as mck:
        main.main(('pr', 'list'))

        mck.assert_called_once()
