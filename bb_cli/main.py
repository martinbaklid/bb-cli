import click

from bb_cli.init import init
from bb_cli.pull_request import pull_request


@click.group()
def main() -> None:
    pass


main.add_command(init)
main.add_command(pull_request)

if __name__ == '__main__':  # pragma: no cover
    main()
