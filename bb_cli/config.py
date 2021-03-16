import os
import sys

import yaml


if sys.version_info >= (3, 8):  # pragma: no cover (<PY38)
    from typing import TypedDict
else:  # pragma: no cover (PY38+)
    from mypy_extensions import TypedDict


APP_NAME = 'bb-cli'
APP_ENV_PREFIX = 'BB_CLI_'


class Config(TypedDict):
    version: int
    host: str
    username: str
    token: str


def exists() -> bool:
    return os.path.exists(path())


def path() -> str:
    if sys.platform.startswith('win'):
        app_dir = os.path.join(os.environ.get('LOCALAPPDATA'), APP_NAME)
    else:
        app_dir = os.path.expanduser(f'~/.{APP_NAME}')
    app_dir = os.environ.get(f'{APP_ENV_PREFIX}APP_DIR', default=app_dir)
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, 'config.yaml')


def dump(config: Config) -> None:
    with open(path(), mode='w') as config_file:
        yaml.safe_dump(config, config_file, sort_keys=False)


def load() -> Config:
    with open(path()) as config_file:
        return yaml.safe_load(config_file)
