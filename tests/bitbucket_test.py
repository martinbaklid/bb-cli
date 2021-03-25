import pytest

from bb_cli.bitbucket import BitbucetException
from bb_cli.bitbucket import Bitbucket
from bb_cli.bitbucket import NoSuchProjectException
from bb_cli.bitbucket import NoSuchRepoException
from testing.mock_requests import FakeResponse
from testing.mock_requests import get_side_effect


def test__get_repos(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
        ): FakeResponse.from_resource(
            'bitbucket_server/fake_proj_repos.json',
        ),
    })
    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    repos = bb.get_repos('fake-proj')

    assert repos[0]['slug'] == 'fake-repo'


def test__get_repos_host_without_schema(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'https://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
        ): FakeResponse.from_resource(
            'bitbucket_server/fake_proj_repos.json',
        ),
    })
    bb = Bitbucket(
        host='fake.bitbucket-server.com',
        username='',
        token='',
    )

    repos = bb.get_repos('fake-proj')

    assert repos[0]['slug'] == 'fake-repo'


def test__get_repos_paged(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
        ): FakeResponse(
            '{'
            '   "size": 2,'
            '   "limit": 2,'
            '   "isLastPage": false,'
            '   "values": ['
            '        { "slug": "fake-repo-0" },'
            '        { "slug": "fake-repo-1" } '
            '   ],'
            '   "start": 0,'
            '   "nextPageStart": 2'
            '}',
        ),
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
            ('start', 2),
        ): FakeResponse(
            '{'
            '   "size": 2,'
            '   "limit": 2,'
            '   "isLastPage": false,'
            '   "values": ['
            '        { "slug": "fake-repo-2" },'
            '        { "slug": "fake-repo-3" } '
            '   ],'
            '   "start": 2,'
            '   "nextPageStart": 4'
            '}',
        ),
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
            ('start', 4),
        ): FakeResponse(
            '{'
            '   "size": 1,'
            '   "limit": 2,'
            '   "isLastPage": true,'
            '   "values": [{ "slug": "fake-repo-4" }],'
            '   "start": 4'
            '}',
        ),
    })
    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    repos = bb.get_repos('fake-proj')

    assert repos[0]['slug'] == 'fake-repo-0'
    assert repos[1]['slug'] == 'fake-repo-1'
    assert repos[2]['slug'] == 'fake-repo-2'
    assert repos[3]['slug'] == 'fake-repo-3'
    assert repos[4]['slug'] == 'fake-repo-4'


def test__get_repos_project_does_not_exists_on_server(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/not-a-project/repos',
        ): FakeResponse(
            '{}',
            status_code=404,
        ),
    })

    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    with pytest.raises(NoSuchProjectException):
        bb.get_repos('not-a-project')


def test__get_repos_server_error(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos',
        ): FakeResponse(
            '{}',
            status_code=500,
        ),
    })

    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    with pytest.raises(BitbucetException):
        bb.get_repos('fake-proj')


def test__get_pull_requests_no_repo_or_project(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/not-a-project/repos/not-a-repo/pull-requests',
        ): FakeResponse(
            '{}',
            status_code=404,
        ),
    })

    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    with pytest.raises(NoSuchRepoException):
        bb.get_pull_requests('not-a-project', 'not-a-repo')


def test__get_pull_requests_server_error(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (
            'http://fake.bitbucket-server.com/rest/api/1.0'
            '/projects/fake-proj/repos/fake-repo/pull-requests',
        ): FakeResponse(
            '{}',
            status_code=500,
        ),
    })

    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    with pytest.raises(BitbucetException):
        bb.get_pull_requests('fake-proj', 'fake-repo')
