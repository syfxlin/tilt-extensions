from api.tilt_extensions import *

load('ext://helm_remote', 'helm_remote')


def component_chart(
        name,                       # type: str
        namespace='',               # type: str
        version='',                 # type: str
        allow_duplicates=False,     # type: bool
        create_namespace=False,     # type: bool
        values=[],                  # type: str | list[str]
        set=[]                      # type: str | list[str]
):
    helm_remote(
        release_name=name,
        namespace=namespace,
        version=version,
        allow_duplicates=allow_duplicates,
        create_namespace=create_namespace,
        values=values,
        set=set,
        chart='component-chart',
        repo_url='https://charts.devspace.sh',
    )
