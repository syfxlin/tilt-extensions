from write_file import *
from api.tilt_extensions import *

load('../write_file/Tiltfile', 'write_file')


def _namespace_inject(
    x,                                  # type: Blob
    ns                                  # type: str
):
    objects = decode_yaml_stream(x)
    for o in objects:
        if type(o) == 'dict' and type(o.get('metadata', None)) == 'dict':
            o['metadata']['namespace'] = ns
    return encode_yaml_stream(objects)


def helm_template(
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
    skip_tls_verify=False,              # type: bool
    username='',                        # type: str
    password='',                        # type: str
    flags=[],                           # type: list[str]
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
        command += ['--create-namespace']
    if include_crds:
        command += ['--include-crds']
    if skip_tls_verify:
        command += ['--insecure-skip-tls-verify']
    if username:
        command += ['--username', username]
    if password:
        command += ['--password', password]
    command += flags
    b = local(command, quiet=True)
    if namespace:
        b = _namespace_inject(b, namespace)
    return b
