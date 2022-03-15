from write_file import *
from api.tilt_extensions import *

load('ext://helm_remote', 'helm_remote')
load('../write_file/Tiltfile', 'write_file')


def helm_create(
        name,
        chart,
        repo_url='',
        repo_name='',
        values_contents='',
        values=[],
        set=[],
        namespace='',
        version='',
        username='',
        password='',
        allow_duplicates=False,
        create_namespace=False
):
    if values_contents != '':
        values = values + [write_file(values_contents)]
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
