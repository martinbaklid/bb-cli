import urllib.parse

import click

from bb_cli import git
from bb_cli.bitbucket import Bitbucket
from bb_cli.config import load_config


@click.group(name='pr')
def pull_request() -> None:
    pass


@pull_request.command(name='list')
def list_all() -> None:
    try:
        remote_url = git.remote_get_url('origin')
    except git.NoRepoException:
        raise click.ClickException('not a git repository')
    except git.NoSuchRemoteException:
        raise click.ClickException('no git remote named origin found')

    url_comps = urllib.parse.urlsplit(remote_url)
    project, repo = url_comps.path[1:-4].split('/')
    config = load_config()
    bitbucket = Bitbucket(
        host=config['host'],
        username=config['username'],
        token=config['token'],
    )
    pull_requests = bitbucket.get_pull_requests(project, repo)
    click.echo(f'Pull requests for {repo}:')
    for pull_request in pull_requests:
        click.echo(
            f'#{pull_request["id"]}: {pull_request["title"]} '
            f'({pull_request["fromRef"]["displayId"]} ->'
            f' {pull_request["toRef"]["displayId"]})',
        )
