from click.testing import CliRunner

from bb_cli.pull_request import list_all
from testing import git
from testing.mock_requests import FakeResponse
from testing.mock_requests import get_side_effect


def test__list_all(mock_requests_get, mock_load_config):
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

    runner = CliRunner()
    with runner.isolated_filesystem():
        git.init()
        git.remote_add('origin', REMOTE_URL)

        res = runner.invoke(list_all)

    assert res.stdout == (
        'Pull requests for fake-repo:\n'
        '#3: feat: add readme (feature/readme -> master)\n'
        '#5: fix: fix typo in readme (bugfix/typo -> master)\n'
    )


def test__list_all_no_git_repo():
    runner = CliRunner(mix_stderr=False)
    with runner.isolated_filesystem():
        res = runner.invoke(list_all)

    assert res.exit_code != 0
    assert len(res.stdout) == 0
    assert res.stderr == (
        'Error: not a git repository\n'
    )


def test__list_all_no_origin():
    runner = CliRunner(mix_stderr=False)
    with runner.isolated_filesystem():
        git.init()

        res = runner.invoke(list_all)
        print(res.stdout)
        print(res.stderr)

    assert res.exit_code != 0
    assert len(res.stdout) == 0
    assert res.stderr == (
        'Error: no git remote named origin found\n'
    )
