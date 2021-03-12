import os
import subprocess
from typing import Optional

import click

import bb_cli.config
from bb_cli.bitbucket import Bitbucket


def _git(*cmd: str, wdir: Optional[str] = None) -> bool:
    wdir_args = ('-C', wdir) if wdir else ()
    res = subprocess.run(('git', *wdir_args, *cmd), stdout=subprocess.DEVNULL)
    return res.returncode == 0


@click.command()
def clone() -> None:
    config = bb_cli.config.load()
    bitbucket = Bitbucket(
        host=config['host'],
        username=config['username'],
        token=config['token'],
    )
    for project in config['projects']:
        project_dir_name = project['slug'].lower().replace('_', '-')
        project_dir_path = os.path.join(
            os.path.expanduser(config['projects_folder']), project_dir_name,
        )
        os.makedirs(project_dir_path, exist_ok=True)
        repos = bitbucket.get_repos(project['slug'])
        click.secho(f"Cloning {project['slug']} repos", fg='blue', bold=True)
        for repo in repos:
            clone_urls = {
                link['name']: link['href']
                for link in repo['links']['clone']
            }

            repo_path = os.path.join(project_dir_path, repo['slug'])
            is_repo = _git(
                'rev-parse', '--is-inside-work-tree', wdir=repo_path,
            )
            if os.path.exists(repo_path) and is_repo:
                click.secho(
                    f"Repo {repo['slug']} is allready cloned",
                    fg='yellow',
                    bold=True,
                )
                continue

            click.secho(f"Cloning {repo['slug']}", fg='blue', bold=True)
            res = _git('clone', clone_urls['ssh'], repo_path)
            if not res:
                click.secho(
                    f"Failed to clone {repo['slug']}", fg='red', err=True,
                )

        click.echo()
