from api import *
import os


def dotenv(
    file='.env'     # type: str
):
    f = read_file(file)
    lines = str(f).splitlines()
    for line in lines:
        v = line.split('=', 1)
        if len(v) < 2:
            continue
        os.putenv(v[0], v[1])
    return os.environ
