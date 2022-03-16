from write_file import *
from api.tilt_extensions import *

load('ext://helm_remote', 'helm_remote')
load('../write_file/Tiltfile', 'write_file')


def helm_create(
    name,                       # type: str
    chart,                      # type: str
    repo_url='',                # type: str
    repo_name='',               # type: str
    values_contents='',         # type: str | dict[str, Any] | list[Any]
    values=[],                  # type: list[str]
    set=[],                     # type: list[str]
    namespace='',               # type: str
    version='',                 # type: str
    username='',                # type: str
    password='',                # type: str
    allow_duplicates=False,     # type: bool
    create_namespace=False      # type: bool
):
    if values_contents != '':
        if type(values_contents) == 'string':
            values = values + [write_file(values_contents)]
        else:
            values = values + [write_file(str(encode_yaml(values_contents)))]
    return helm_remote(
        release_name=name,
        chart=chart,
        repo_url=repo_url,
        repo_name=repo_name,
        values=values,
        set=set,
        namespace=namespace,
        version=version,
        username=username,
        password=password,
        allow_duplicates=allow_duplicates,
        create_namespace=create_namespace
    )
