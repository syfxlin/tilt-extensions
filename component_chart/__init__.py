from helm_create import *

load('../helm_create/Tiltfile', 'helm_create')


def component_chart(
        name,                       # type: str
        namespace='',               # type: str
        version='',                 # type: str
        allow_duplicates=False,     # type: bool
        create_namespace=False,     # type: bool
        values_contents='',         # type: str
        values=[],                  # type: str | list[str]
        set=[]                      # type: str | list[str]
):
    helm_create(
        name=name,
        namespace=namespace,
        version=version,
        allow_duplicates=allow_duplicates,
        create_namespace=create_namespace,
        values_contents=values_contents,
        values=values,
        set=set,
        chart='component-chart',
        repo_url='https://charts.devspace.sh',
    )
