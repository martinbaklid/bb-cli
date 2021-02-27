import click
import urllib.parse

from click.utils import echo

from bb_cli import custom_types
from bb_cli.config import Config, ProjectConfig, dump_config, config_path, config_exists

import requests


@click.command()
def init() -> None:
    """ Interactive initialization Bitbucket CLI """
    if config_exists():
        raise click.ClickException(
            f"Config allready exsists in {config_path()}. To change the configuration use {click.style('bb-cli conifg edit', bold=True)}"
        )

    click.secho("Welcome to Bitbucket CLI", fg="blue", bold=True)
    click.secho("Starting first time configuration", fg="blue", bold=True)
    host = click.prompt(
        click.style(
            "Provide the hostname (with protocol prefix) for your bitbucket server (eg. https://company.bitbucket-server.com)",
            bold=True,
        ),
        type=custom_types.HOST,
    )
    host = urllib.parse.urljoin("https://", host)

    username = click.prompt(click.style(f"Provide your username", bold=True))

    token_gen_url = urllib.parse.urljoin(host, "plugins/servlet/access-tokens/manage")
    click.secho(
        "To use BitBucket CLI you need to provide personal api token with read premisions.",
        fg="blue",
        bold=True,
    )
    click.secho(
        f'    1. Go to {token_gen_url} and click "Create a token"', fg="blue", bold=True
    )
    click.secho(
        f'    2. Set an appropriate "Token name" and give the token "Read Premisions"',
        fg="blue",
        bold=True,
    )
    click.secho(f"    3. Click create and copy the token", fg="blue", bold=True)
    token = click.prompt(click.style("Paste your token here", bold=True))

    include_personal_repos = click.prompt(
        click.style("Do you want your personal repos managed (yes/no)", bold=True),
        type=click.BOOL,
        default="yes",
    )

    projects_folder = click.prompt(
        click.style("Where do you want the Bitbucket projects cloned", bold=True),
        type=click.Path(),
        default="~/projects",
        show_default=True,
    )

    project_slugs = click.prompt(
        f'{click.style("List the project slugs of the projects you want manage",  bold=True)} (eg. "PROJ_SLUG1 PROJ_SLUG2")',
        type=custom_types.SPACE_SEP_LIST,
    )

    initial_config: Config = dict(
        version=1,
        host=host,
        username=username,
        token=token.strip(),
        include_personal_repos=include_personal_repos,
        projects_folder=projects_folder,
        projects=[dict(slug=slug) for slug in project_slugs],
    )
    dump_config(initial_config)
    click.secho(f"Config initialized in {config_path()}:", fg="green", bold=True)
    click.secho(
        f'To change configuration use "bb-cli config edit"', fg="blue", bold=True
    )
