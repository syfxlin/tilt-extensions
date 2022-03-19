from helm_template import *

load('../helm_template/Tiltfile', 'helm_template')


def component_chart(
    name,                       # type: str
    values_contents='',         # type: str | dict[str, Any] | list[Any]
    values=[],                  # type: list[str]
    set=[],                     # type: list[str]
    namespace='',               # type: str
    version='',                 # type: str
    flags=[],                   # type: list[str]
):
    return helm_template(
        name=name,
        values_contents=values_contents,
        values=values,
        set=set,
        namespace=namespace,
        version=version,
        chart='component-chart',
        repo='https://charts.devspace.sh',
        api_versions=['networking.k8s.io/v1/Ingress'],
        kube_version='1.22.7',
        flags=flags
    )
