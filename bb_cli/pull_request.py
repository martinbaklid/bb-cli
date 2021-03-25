import sys
import urllib.parse

import bb_cli.config
from bb_cli import git
from bb_cli.bitbucket import Bitbucket
from bb_cli.bitbucket import NoSuchRepoException


def list_all() -> int:
    try:
        remote_url = git.remote_get_url('origin')
    except git.NoRepoException:
        print('Error: not a git repository', file=sys.stderr)
        return 1
    except git.NoSuchRemoteException:
        print('Error: no git remote named origin found', file=sys.stderr)
        return 1

    url_comps = urllib.parse.urlsplit(remote_url)
    project, repo = url_comps.path[1:-4].split('/')
    config = bb_cli.config.load()
    if url_comps.hostname != urllib.parse.urlparse(config['host']).netloc:
        print(
            f'Error: No host named {url_comps.hostname} in the config',
            file=sys.stderr,
        )
        return 1

    bitbucket = Bitbucket(
        host=config['host'],
        username=config['username'],
        token=config['token'],
    )
    try:
        pull_requests = bitbucket.get_pull_requests(project, repo)
    except NoSuchRepoException:
        print(
            f'Error: Did not find the repossitory {repo} '
            f'for project {project}',
            file=sys.stderr,
        )
        return 1

    print(f'Pull requests for {repo}:')
    for pull_request in pull_requests:
        print(
            f'#{pull_request["id"]}: {pull_request["title"]} '
            f'({pull_request["fromRef"]["displayId"]} ->'
            f' {pull_request["toRef"]["displayId"]})',
        )
    return 0
