import click
from bb_cli.init import init
from bb_cli.config import config, APP_NAME
from bb_cli.clone import clone


@click.group()
def cli() -> None:
    pass


def main() -> None:
    cli.add_command(init)
    cli.add_command(config)
    cli.add_command(clone)
    cli()


if __name__ == "__main__":
    main()
