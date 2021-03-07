import click

from bb_cli.clone import clone
from bb_cli.config import config
from bb_cli.init import init
from bb_cli.pull_request import pull_request


@click.group()
def cli() -> None:
    pass


def main() -> None:
    cli.add_command(init)
    cli.add_command(config)
    cli.add_command(clone)
    cli.add_command(pull_request)
    cli()


if __name__ == '__main__':
    main()
