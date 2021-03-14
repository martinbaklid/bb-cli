import sys
import urllib.parse

import click

import bb_cli.config
from bb_cli import cli
from bb_cli.config import Config


def _init() -> None:
    """ Interactive initialization Bitbucket CLI """
    if bb_cli.config.exists():
        print(
            f'Error: Config allready exsists in {bb_cli.config.path()}. '
            'To change the configuration use bb-cli conifg edit',
            file=sys.stderr,
        )
        exit(1)

    print('Welcome to Bitbucket CLI')
    print('Starting first time configuration')
    host = cli.prompt(
        'Provide the url to your bitbucket server\n'
        '(eg. https://company.bitbucket-server.com):\n',
    )
    host = urllib.parse.urljoin('https://', host)

    username = cli.prompt('Provide your username:\n')

    token_gen_url = urllib.parse.urljoin(
        host, 'plugins/servlet/access-tokens/manage',
    )
    token = cli.prompt(
        'BitBucket CLI needs a personal api token with read premisions.\n'
        f'    1. Go to {token_gen_url}\n'
        '    2. Click "Create a token"\n'
        '    3. Set "Token name" and select "Read Premisions"\n'
        '    4. Click create and copy the token\n'
        'Paste your token here:\n',
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


@click.command(name='click')
def init() -> None:
    _init()
