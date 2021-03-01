from bb_cli.bitbucket import Bitbucket
from testing.mock_requests import FakeResponse
from testing.mock_requests import get_side_effect

FAKE_PROJ_REPOS = (
    'http://fake.bitbucket-server.com/rest/api/1.0'
    '/projects/fake_proj/repos'
)


def test__get_repos(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (FAKE_PROJ_REPOS,): FakeResponse.from_resource(
            'bitbucket_server/fake_proj_repos.json',
        ),
    })
    bb = Bitbucket(
        host='http://fake.bitbucket-server.com',
        username='',
        token='',
    )

    repos = bb.get_repos('fake_proj')

    assert repos[0]['slug'] == 'fake-repo'


def test__get_repos_paged(mock_requests_get):
    mock_requests_get.side_effect = get_side_effect({
        (FAKE_PROJ_REPOS,): FakeResponse(
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
        (FAKE_PROJ_REPOS, ('start', 2)): FakeResponse(
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
        (FAKE_PROJ_REPOS, ('start', 4)): FakeResponse(
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

    repos = bb.get_repos('fake_proj')

    assert repos[0]['slug'] == 'fake-repo-0'
    assert repos[1]['slug'] == 'fake-repo-1'
    assert repos[2]['slug'] == 'fake-repo-2'
    assert repos[3]['slug'] == 'fake-repo-3'
    assert repos[4]['slug'] == 'fake-repo-4'
