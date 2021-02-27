import click
from click.core import Option
import yaml
import os

from typing import Any, Dict, List, NamedTuple, Optional, TypedDict

APP_NAME = "bb-cli"
ENV_PREFIX = "BB_CLI_"


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
    return os.environ.get(ENV_PREFIX + key, default)


def config_exists() -> bool:
    return os.path.exists(config_path())


def config_path() -> str:
    click_default = click.get_app_dir(APP_NAME, force_posix=True)
    app_dir = app_environ("APP_DIR", default=click_default)
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "config.yaml")


def dump_config(config: Config) -> None:
    with open(config_path(), mode="w") as config_file:
        yaml.safe_dump(config, config_file, sort_keys=False)


def load_config() -> Config:
    with open(config_path()) as config_file:
        return yaml.safe_load(config_file)


@click.group()
def config() -> None:
    pass


@config.command()
def edit() -> None:
    """ opens config file in editor """
    if not os.path.exists(config_path()):
        raise click.ClickException(f"Can't find config file in {config_path()}")
    click.edit(filename=config_path())
