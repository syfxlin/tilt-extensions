from api import *


def mk_temp():         # type: (...) -> str
    path = str(local(
        command='echo $(mktemp -u)',
        command_bat='echo %TMP%/tmp.%RANDOM%%RANDOM%',
        quiet=True
    )).strip()
    print(path)
    return path


def write_file(
    contents,               # type: str
    path=''                 # type: str
):                          # type: (...) -> str
    if path == '':
        path = mk_temp()
    local(
        command='echo "$CONTENTS" > "$FILENAME"',
        command_bat='echo %CONTENTS% > %FILENAME%',
        env={'CONTENTS': contents, 'FILENAME': path},
        quiet=True
    )
    return path
