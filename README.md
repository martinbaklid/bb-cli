# BB-CLI
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/martinbaklid/bb-cli/main.svg?badge_token=kdBJoLnlSuOz-j78Wndqdg)](https://results.pre-commit.ci/badge/github/martinbaklid/bb-cli/main.svg?badge_token=kdBJoLnlSuOz-j78Wndqdg)
[![codecov](https://codecov.io/gh/martinbaklid/bb-cli/branch/main/graph/badge.svg?token=IZYKY0RNSR)](https://codecov.io/gh/martinbaklid/bb-cli)

Bitbucket Server CLI to manage repossitories from the comfort of your command line. Inspired by the design of GitHub CLI.

## Currently suported features
### Pull requests

```shell
$ bb-cli pr list # lists pr for current repo
```

## Configuration
Configuration is by default stored in `~/.bb-cli/config.yml` on unix like systems.

```yml
version: 1
host: http(s)://<bitbucket-host> # Host of the bitbucket server
username: <username> # Bitbucket server username
token: <personal-access-token> # Personal access token. Can be generated from http(s)://<bitbucket-host>/plugins/servlet/access-tokens/manage
```
