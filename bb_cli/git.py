import subprocess


class GitException(Exception):
    pass


class NoRepoException(GitException):
    def __str__(self) -> str:
        return 'The current working directory is not a git repossitory'


class NoSuchRemoteException(GitException):
    def __init__(self, remote: str, *args: object) -> None:
        self.remote = remote

    def __str__(self) -> str:
        return f'No remote named {self.remote}'


NO_SUCH_REMOTE_RETURN_CODE = 2


def remote_get_url(remote: str) -> str:
    check_is_git_repo()
    res = subprocess.run(
        ('git', 'remote', 'get-url', remote),
        capture_output=True,
    )
    # https://git-scm.com/docs/git-remote#_exit_status
    if res.returncode == NO_SUCH_REMOTE_RETURN_CODE:
        raise NoSuchRemoteException(remote)

    return res.stdout.decode().strip()


def check_is_git_repo() -> None:
    try:
        subprocess.run(
            ('git', 'rev-parse', '--is-inside-work-tree'),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        raise NoRepoException()
