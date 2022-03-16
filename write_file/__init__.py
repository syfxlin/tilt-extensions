import os
from api import *

cwd = os.getcwd()


def mk_temp():         # type: (...) -> str
    path = str(local(
        command='echo $(mktemp -u)',
        command_bat='echo %TMP%/tmp.%RANDOM%%RANDOM%',
        quiet=True
    )).strip()
    return path


def write_file(
    contents,               # type: str
    path=''                 # type: str
):                          # type: (...) -> str
    if path == '':
        path = mk_temp()
    local(
        command='sh {}'.format(os.path.join(cwd, 'write_file.sh')),
        command_bat='powershell.exe {}'.format(os.path.join(cwd, 'write_file.ps1')),
        env={'CONTENTS': contents, 'FILENAME': path},
        quiet=True
    )
    return path
