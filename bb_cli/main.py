import argparse
from typing import Optional
from typing import Sequence

from bb_cli.init import init
from bb_cli.pull_request import list_all


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog='bb-cli')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    subparsers.add_parser('init', help='Initialize bb-cli')
    parser_pr = subparsers.add_parser(
        'pr', help='Work with BitBucket pull requests',
    )
    subparsers_pr = parser_pr.add_subparsers(dest='pr_command')
    subparsers_pr.required = True
    subparsers_pr.add_parser('list')

    args = parser.parse_args(argv)

    if args.command == 'init':
        return init()
    elif args.command == 'pr':
        if args.pr_command == 'list':
            return list_all()
        else:
            raise NotImplementedError(
                f'PR command {args.pr_command} not implemented.',
            )
    else:
        raise NotImplementedError(f'Command {args.command} not implemented.')


if __name__ == '__main__':  # pragma: no cover
    exit(main())
