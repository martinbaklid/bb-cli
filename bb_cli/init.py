import urllib.parse

import click
from click import ClickException
from click import style

from bb_cli import custom_types
from bb_cli.config import Config
from bb_cli.config import config_exists
from bb_cli.config import config_path
from bb_cli.config import dump_config


@click.command()
def init() -> None:
    """ Interactive initialization Bitbucket CLI """
    if config_exists():
        raise ClickException(
            f'Config allready exsists in {config_path()}. '
            'To change the configuration use '
            f'{style("bb-cli conifg edit", bold=True)}',
        )

    click.secho('Welcome to Bitbucket CLI', fg='blue', bold=True)
    click.secho('Starting first time configuration', fg='blue', bold=True)
    host = click.prompt(
        style(
            'Provide the url to your bitbucket server\n'
            '(eg. https://company.bitbucket-server.com)',
            bold=True,
        ),
        type=custom_types.HOST,
        prompt_suffix=':\n',
    )
    host = urllib.parse.urljoin('https://', host)

    username = click.prompt(
        style('Provide your username', bold=True),
        prompt_suffix=':\n',
    )

    token_gen_url = urllib.parse.urljoin(
        host, 'plugins/servlet/access-tokens/manage',
    )
    click.secho(
        'BitBucket CLI needs a personal api token with read premisions.',
        fg='blue',
        bold=True,
    )
    click.secho(
        f'    1. Go to {token_gen_url}',
        fg='blue',
        bold=True,
    )
    click.secho(
        '    2. Click "Create a token"',
        fg='blue',
        bold=True,
    )
    click.secho(
        '    3. Set "Token name" and select "Read Premisions"',
        fg='blue',
        bold=True,
    )
    click.secho(
        '    4. Click create and copy the token',
        fg='blue', bold=True,
    )
    token = click.prompt(
        style('Paste your token here', bold=True),
        prompt_suffix=':\n',
    )

    include_personal_repos = click.prompt(
        style(
            'Do you want your personal repos managed (yes/no)', bold=True,
        ),
        type=click.BOOL,
        default='yes',
        prompt_suffix=':\n',
    )

    projects_folder = click.prompt(
        style(
            'Where do you want the Bitbucket projects cloned', bold=True,
        ),
        type=click.Path(),
        default='~/projects',
        show_default=True,
        prompt_suffix=':\n',
    )

    project_slugs = click.prompt(
        f'{style("List the slugs of projects you want manage",  bold=True)}\n'
        '(eg. "PROJ_SLUG1 PROJ_SLUG2")',
        type=custom_types.SPACE_SEP_LIST,
        prompt_suffix=':\n',
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
    click.secho(
        f'Config initialized in {config_path()}:',
        fg='green',
        bold=True,
    )
    click.secho(
        'To change configuration use "bb-cli config edit"',
        fg='blue',
        bold=True,
    )
