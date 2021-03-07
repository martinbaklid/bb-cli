# BB-CLI

## Pull requests

```shell
$ bb-cli pr list # reads the current directorys git folder and lists all pr for repo
```


## Configuration

```yml
# Stored in .bb-cli/config.yml
version: 1
host: http(s)://<bitbucket-host> # Host of the bitbucket server
username: <username> # Bitbucket server username
token: <personal-access-token> # Personal access token. Can be generated from http(s)://<bitbucket-host>/plugins/servlet/access-tokens/manage
include_personal_repos: ( true | false ) # (Optinal, defualt: false) Will include the personal repos i.e, repos visible on personal repos http(s)://<bitbucket-host>/profile
projects_folder: <local path> # Where all the projects are stored
projects: # List of projects
- slug: <project-slug> # http(s)://<bitbucket-host>/projects/<project-slug>
  folder_name: <folder name> # (Optional)
  exclude_repos:
  - <repo-slug> # List all <repo-slug>s for all repos in project with slug <project-slug> that should be excluded
```

### Example
*Given*
```yml
version: 1
host: http(s)://example.bitbucket.server
username: olanorman
token: NDc1ODg1ODM5ODI3OsbV7hCjd0zcMO80QV1I1VB3omKn
include_personal_repos: true
projects_folder: ~/projets
projects:
- slug: web
- slug: samp
  folder_name: samples
```
*and web project contianing repos*
- `name: backend server, slug: backend-server`
- `name: frontend, slug: frontend`

*and sample project contianing repo*
- `name: sample-usage, slug: sample-usage`

*and personal projects*
- `name: fun, slug: fun`

*then the resulting folders on local machine will be*
```bash
web/
    # note: the folder name will be the slug, as it would be with git clone.
    #       this can not be overridden
    backend-server/
        ...
    frontend/
        ...
samples/ # name of folder overridden by foldername
    sample-usage/
        ...
olanorman/
    fun/
        ...
```
