import os
import sys

import click
import yaml


if sys.version_info >= (3, 8):  # pragma: no cover (<PY38)
    from typing import TypedDict
else:  # pragma: no cover (PY38+)
    from mypy_extensions import TypedDict


APP_NAME = 'bb-cli'
ENV_PREFIX = 'BB_CLI_'


class Config(TypedDict):
    version: int
    host: str
    username: str
    token: str


def app_environ(key: str, default: str) -> str:
    return os.environ.get(f'{ENV_PREFIX}{key}', default)


def exists() -> bool:
    return os.path.exists(path())


def path() -> str:
    click_default = click.get_app_dir(APP_NAME, force_posix=True)
    app_dir = app_environ('APP_DIR', default=click_default)
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, 'config.yaml')


def dump(config: Config) -> None:
    with open(path(), mode='w') as config_file:
        yaml.safe_dump(config, config_file, sort_keys=False)


def load() -> Config:
    with open(path()) as config_file:
        return yaml.safe_load(config_file)
