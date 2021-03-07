import contextlib
import os
from typing import Generator


@contextlib.contextmanager
def cwd(path: str) -> Generator[None, None, None]:
    pwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(pwd)
