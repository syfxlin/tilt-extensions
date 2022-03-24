from api import *
from api import os
from api.os import path

cwd = os.getcwd()


def write_file(
    contents,               # type: str
    path=''                 # type: str
):                          # type: (...) -> str
    path = str(local(
        command='chmod +x {w}; {w}'.format(w=os.path.join(cwd, 'write_file')),  # linux, amd64
        command_bat=os.path.join(cwd, 'write_file.exe'),  # windows, amd64
        env={
            'CONTENTS': contents,
            'FILENAME': path,
            'ROOT_DIR': os.getenv('TILT_DIR', '')
        },
        quiet=True
    ))
    return path
