import sys
import urllib.parse

import click

import bb_cli.config
from bb_cli import git
from bb_cli.bitbucket import Bitbucket


def _list_all() -> None:
    try:
        remote_url = git.remote_get_url('origin')
    except git.NoRepoException:
        print('Error: not a git repository', file=sys.stderr)
        exit(1)
    except git.NoSuchRemoteException:
        print('Error: no git remote named origin found', file=sys.stderr)
        exit(1)

    url_comps = urllib.parse.urlsplit(remote_url)
    project, repo = url_comps.path[1:-4].split('/')
    config = bb_cli.config.load()
    bitbucket = Bitbucket(
        host=config['host'],
        username=config['username'],
        token=config['token'],
    )
    pull_requests = bitbucket.get_pull_requests(project, repo)
    print(f'Pull requests for {repo}:')
    for pull_request in pull_requests:
        print(
            f'#{pull_request["id"]}: {pull_request["title"]} '
            f'({pull_request["fromRef"]["displayId"]} ->'
            f' {pull_request["toRef"]["displayId"]})',
        )


@click.group(name='pr')
def pull_request() -> None:
    pass


@pull_request.command(name='list')
def list_all() -> None:
    _list_all()
