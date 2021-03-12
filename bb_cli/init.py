import urllib.parse

import click
from click import ClickException
from click import style

import bb_cli.config
from bb_cli import custom_types
from bb_cli.config import Config


@click.command()
def init() -> None:
    """ Interactive initialization Bitbucket CLI """
    if bb_cli.config.exists():
        raise ClickException(
            f'Config allready exsists in {bb_cli.config.path()}. '
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
    bb_cli.config.dump(
        Config(
            version=1,
            host=host,
            username=username,
            token=token.strip(),
        ),
    )
    click.secho(
        f'Config initialized in {bb_cli.config.path()}:',
        fg='green',
        bold=True,
    )
    click.secho(
        'To change configuration use "bb-cli config edit"',
        fg='blue',
        bold=True,
    )
