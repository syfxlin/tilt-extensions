from api import *


def write_temp_file(
    contents            # type: str
):                      # type: (...) -> str
    path = str(local(
        command="""
            FILENAME=$(mktemp -u)
            echo "$CONTENTS" > "$FILENAME"
            echo "$FILENAME"
        """,
        command_bat="""
            @echo off
            :unique
            set "FILENAME=%TMP%/tmp.%RANDOM%%RANDOM%"
            if exist "%FILENAME%" goto :unique
            echo %CONTENTS% > %FILENAME%
            echo %FILENAME%
        """,
        env={'CONTENTS': contents},
        quiet=True
    )).rstrip('\n')
    watch_settings(ignore=path)
    return path


def write_file(
    contents,               # type: str
    path=''                 # type: str
):                          # type: (...) -> str
    if path:
        local(
            command='echo "$CONTENTS" > "$FILENAME"',
            command_bat='echo %CONTENTS% > %FILENAME%',
            env={'CONTENTS': contents, 'FILENAME': path},
            quiet=True
        )
        return path
    else:
        return write_temp_file(contents=contents)
