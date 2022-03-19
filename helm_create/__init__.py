from write_file import *
from api.tilt_extensions import *

load('ext://helm_remote', 'helm_remote')
load('../write_file/Tiltfile', 'write_file')


def helm_create(
    name,                               # type: str
    chart,                              # type: str
    version='',                         # type: str
    namespace='',                       # type: str
    repo='',                            # type: str
    values_contents='',                 # type: str | dict[str, Any] | list[Any]
    values=[],                          # type: list[str]
    set=[],                             # type: list[str]
    api_versions=[],                    # type: list[str]
    kube_version='',                    # type: str
    create_namespace=True,              # type: bool
    include_crds=True,                  # type: bool
    insecure_skip_tls_verify=False,     # type: bool
    username='',                        # type: str
    password='',                        # type: str
    flags=[],                           # type: list[str]
    allow_duplicates=False,             # type: bool
):
    if values_contents != '':
        if type(values_contents) == 'string':
            values = values + [write_file(values_contents)]
        else:
            values = values + [write_file(str(encode_yaml(values_contents)))]
    command = ['helm', 'template', name, chart]
    if version:
        command += ['--version', version]
    if namespace:
        command += ['--namespace', namespace]
    if repo:
        command += ['--repo', repo]
    for value in values:
        command += ['--values', value]
    for value in set:
        command += ['--set', value]
    for value in api_versions:
        command += ['--api-versions', value]
    if kube_version:
        command += ['--kube-version', kube_version]
    if create_namespace:
        command += ['--create-namespace', create_namespace]
    if include_crds:
        command += ['--include-crds']
    if insecure_skip_tls_verify:
        command += ['--insecure-skip-tls-verify']
    if username:
        command += ['--username', username]
    if password:
        command += ['--password', password]
    command += flags

    yaml = str(local(command))
    k8s_yaml(yaml, allow_duplicates=allow_duplicates)
    return yaml
