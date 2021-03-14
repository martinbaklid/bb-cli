import urllib.parse

import click
from click import style

import bb_cli.config
from bb_cli import custom_types
from bb_cli.config import Config


@click.command()
def init() -> None:
    """ Interactive initialization Bitbucket CLI """
    if bb_cli.config.exists():
        print(
            f'Error: Config allready exsists in {bb_cli.config.path()}. '
            'To change the configuration use bb-cli conifg edit',
        )
        exit(1)

    print('Welcome to Bitbucket CLI')
    print('Starting first time configuration')
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
    print('BitBucket CLI needs a personal api token with read premisions.')
    print(f'    1. Go to {token_gen_url}')
    print('    2. Click "Create a token"')
    print('    3. Set "Token name" and select "Read Premisions"')
    print('    4. Click create and copy the token')

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
    print(f'Config initialized in {bb_cli.config.path()}:')
    print('To change configuration use "bb-cli config edit"')
