import pytest

import testing.git
from bb_cli import git
from testing import os_utils


def test__remote_get_url(tmp_path):
    REMOTE = 'http://example.com/project/repo.git'
    with os_utils.cwd(tmp_path):
        testing.git.init()
        testing.git.remote_add('origin', REMOTE)

        res = git.remote_get_url('origin')

    assert res == REMOTE


def test__remote_get_url_no_git_repo(tmp_path):
    with os_utils.cwd(tmp_path), pytest.raises(git.NoRepoException) as excinfo:
        git.remote_get_url('origin')

    assert str(excinfo.value) == (
        'The current working directory is not a git repossitory'
    )


def test__remote_get_url_no_remote_origin(tmp_path):
    with os_utils.cwd(tmp_path), \
            pytest.raises(git.NoSuchRemoteException) as excinfo:
        testing.git.init()

        git.remote_get_url('origin')

    assert excinfo.value.remote == 'origin'
    assert str(excinfo.value) == (
        'No remote named origin'
    )
