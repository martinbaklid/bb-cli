import subprocess


def init():
    subprocess.run(
        ('git', 'init'),
        check=True,
    )


def remote_add(name, url):
    subprocess.run(
        ('git', 'remote', 'add', name, url),
        check=True,
    )
