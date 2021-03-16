from bb_cli.pull_request import list_all
from testing import git
from testing import os_utils
from testing.mock_requests import FakeResponse
from testing.mock_requests import get_side_effect


def test__list_all(mock_requests_get, mock_load_config, tmp_path, capsys):
    PR_URL = (
        'http://company.bitbucket.com/rest/api/1.0'
        '/projects/fake_proj/repos/fake-repo/pull-requests'
    )
    REMOTE_URL = 'ssh://git@company.bitbucket.com/fake_proj/fake-repo.git'

    def load_config():
        return {
            'host': 'http://company.bitbucket.com',
            'username': 'user',
            'token': 'token',
        }
    mock_load_config.side_effect = load_config

    mock_requests_get.side_effect = get_side_effect({
        (PR_URL,): FakeResponse(
            '{'
            '    "size": 2,'
            '    "limit": 25,'
            '    "isLastPage": true,'
            '    "values": ['
            '        {'
            '            "id": 3,'
            '            "version": 0,'
            '            "title": "feat: add readme",'
            '            "description": "",'
            '            "state": "OPEN",'
            '            "open": true,'
            '            "closed": false,'
            '            "createdDate": 1614546563947,'
            '            "updatedDate": 1614546563947,'
            '            "fromRef": {'
            '               "id": "refs/heads/feature/readme",'
            '               "displayId": "feature/readme"'
            '            },'
            '            "toRef": {'
            '               "id": "refs/heads/master",'
            '               "displayId": "master"'
            '            }'
            '        },'
            '        {'
            '            "id": 5,'
            '            "version": 0,'
            '            "title": "fix: fix typo in readme",'
            '            "description": "",'
            '            "state": "OPEN",'
            '            "open": true,'
            '            "closed": false,'
            '            "createdDate": 1614546563947,'
            '            "updatedDate": 1614546563947,'
            '            "fromRef": {'
            '               "id": "refs/heads/bugfix/typo",'
            '               "displayId": "bugfix/typo"'
            '            },'
            '            "toRef": {'
            '               "id": "refs/heads/master",'
            '               "displayId": "master"'
            '            }'
            '        }'
            '    ]'
            '}',
        ),
    })

    with os_utils.cwd(tmp_path):
        git.init()
        git.remote_add('origin', REMOTE_URL)

        list_all()

    out, _ = capsys.readouterr()
    assert out == (
        'Pull requests for fake-repo:\n'
        '#3: feat: add readme (feature/readme -> master)\n'
        '#5: fix: fix typo in readme (bugfix/typo -> master)\n'
    )


def test__list_all_no_git_repo(tmp_path, capsys):
    with os_utils.cwd(tmp_path):
        return_code = list_all()

    _, err = capsys.readouterr()
    assert return_code == 1
    assert err == (
        'Error: not a git repository\n'
    )


def test__list_all_no_origin(tmp_path, capsys):
    with os_utils.cwd(tmp_path):
        git.init()

        return_code = list_all()

    _, err = capsys.readouterr()
    assert return_code == 1
    assert err == (
        'Error: no git remote named origin found\n'
    )
