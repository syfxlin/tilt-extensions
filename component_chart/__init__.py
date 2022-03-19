from helm_create import *

load('../helm_create/Tiltfile', 'helm_create')


def component_chart(
    name,                       # type: str
    values_contents='',         # type: str | dict[str, Any] | list[Any]
    values=[],                  # type: list[str]
    set=[],                     # type: list[str]
    namespace='',               # type: str
    version='',                 # type: str
    flags=[],                   # type: list[str]
    allow_duplicates=False,     # type: bool
):
    helm_create(
        name=name,
        values_contents=values_contents,
        values=values,
        set=set,
        namespace=namespace,
        version=version,
        allow_duplicates=allow_duplicates,
        chart='component-chart',
        repo='https://charts.devspace.sh',
        api_versions=['networking.k8s.io/v1/Ingress'],
        kube_version='1.22.7',
        flags=flags
    )