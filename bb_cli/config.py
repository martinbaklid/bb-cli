import os
from typing import List

import click
import yaml


try:
    from typing import TypedDict
except ImportError:
    from mypy_extensions import TypedDict


APP_NAME = 'bb-cli'
ENV_PREFIX = 'BB_CLI_'


class ProjectConfig(TypedDict):
    slug: str


class Config(TypedDict):
    version: int
    host: str
    username: str
    token: str
    include_personal_repos: bool
    projects_folder: str
    projects: List[ProjectConfig]


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


@click.group()
def config() -> None:
    pass


@config.command()
def edit() -> None:
    """ opens config file in editor """
    if not os.path.exists(path()):
        raise click.ClickException(
            f"Can't find config file in {path()}",
        )
    click.edit(filename=path())
