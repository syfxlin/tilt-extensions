from helm_template import *
from kubectl_build import *

load('../helm_template/Tiltfile', 'helm_template')
load('../kubectl_build/Tiltfile', 'kubectl_build')


def _parse_env(env):
    # type: (list[str]) -> dict
    if len(env) >= 3:
        key = env[0]
        ref = env[1]
        if ref == '@configMap' or ref == '@cm':
            [_, _, n, k] = env
            return {
                'name': key,
                'valueFrom': {
                    'secretKeyRef': {
                        'name': n,
                        'key': k
                    }
                }
            }
        elif ref == '@secret' or ref == '@sec':
            [_, _, n, k] = env
            return {
                'name': key,
                'valueFrom': {
                    'configMapKeyRef': {
                        'name': n,
                        'key': k
                    }
                }
            }
        elif ref == '@field':
            [_, _, v] = env
            return {
                'name': key,
                'valueFrom': {
                    'fieldRef': {
                        'fieldPath': v
                    }
                }
            }
        elif ref == '@resource':
            [_, _, v] = env
            return {
                'name': key,
                'valueFrom': {
                    'resourceFieldRef': {
                        'resource': v
                    }
                }
            }
    [key, value] = env
    return {
        'name': key,
        'value': value
    }


def _parse_volume(volume):
    # type: (list[str]) -> (dict, dict)
    name = volume[0]
    path = volume[1]
    drive = volume[2]
    if drive == '@emptyDir':
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name
                }
            },
            {
                'name': name,
                'emptyDir': {}
            }
        )
    elif drive == '@configMap' or drive == '@cm':
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name
                }
            },
            {
                'name': name,
                'configMap': {
                    'name': volume[3]
                }
            }
        )
    elif drive == '@secret' or drive == '@sec':
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name
                }
            },
            {
                'name': name,
                'secret': {
                    'secretName': volume[3]
                }
            }
        )
    elif len(volume) == 3:
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name
                }
            },
            {
                'name': name,
                'size': drive
            }
        )
    elif len(volume) == 4:
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name
                }
            },
            {
                'name': name,
                'storageClassName': drive,
                'size': volume[3]
            }
        )
    else:
        return (
            {
                'containerPath': path,
                'volume': {
                    'name': name,
                    'subPath': volume[4]
                }
            },
            {
                'name': name,
                'storageClassName': drive,
                'size': volume[3]
            }
        )


def _parse_port(port):
    # type: (int | list[int, int] | list[int, int, str]) -> dict
    if type(port) == 'int':
        return {
            'port': port,
        }
    elif len(port) == 2:
        return {
            'port': port[0],
            'containerPort': port[1]
        }
    else:
        return {
            'port': port[0],
            'containerPort': port[1],
            'protocol': port[2]
        }


def _parse_ingress(ingress):
    # type: (str | list[str]) -> dict
    if type(ingress) == 'string':
        return {
            'host': ingress
        }
    elif len(ingress) == 2:
        return {
            'host': ingress[0],
            'path': ingress[1]
        }
    elif len(ingress) == 3:
        return {
            'host': ingress[0],
            'path': ingress[1],
            'pathType': ingress[2]
        }
    else:
        return {
            'host': ingress[0],
            'path': ingress[1],
            'pathType': ingress[2],
            'servicePort': ingress[3]
        }


def deployment(
    # base
    name,                       # type: str
    image,                      # type: str
    registry_secret='',         # type: str
    namespace='',               # type: str
    # deployment config
    command=[],                 # type: list[str]
    args=[],                    # type: list[str]
    env=[],                     # type: list[list[str]]
    volumes=[],                 # type: list[list[str]]
    ports=[],                   # type: list[int | list[int, int] | list[int, int, str]]
    ingress=[],                 # type: list[str | list[str]]
    ingress_class='nginx',      # type: str
    ingress_tls=False,          # type: bool | str
    ingress_config={},          # type: dict[str, str]
    labels={},                  # type: dict[str, str]
    annotations={},             # type: dict[str, str]
    # kubectl build config
    build=True,                 # type: bool
    context='.',                # type: str
    dockerfile='',              # type: str
    dockerfile_contents='',     # type: str
    build_args={},              # type: dict[str, str]
    build_secrets=[],           # type: list[str]
    build_labels={},            # type: dict[str, str]
    build_tags=[],              # type: list[str]
    build_flags=[],             # type: list[str]
    # helm template config
    deploy=True,                # type: bool
    deploy_version='',          # type: str
    deploy_values=[],           # type: list[str]
    deploy_set=[],              # type: list[str]
    deploy_flags=[],            # type: list[str]
    allow_duplicates=False,     # type: bool
):
    values = {
        'containers': [{
            'name': name,
            'image': image,
        }]
    }
    if len(command):
        values['containers'][0]['command'] = command
    if len(args):
        values['containers'][0]['args'] = args
    if len(env):
        values['containers'][0]['env'] = [_parse_env(e) for e in env]
    if len(volumes):
        vs = [_parse_volume(v) for v in volumes]
        values['containers'][0]['volumeMounts'] = [v[0] for v in vs]
        values['volumes'] = [v[1] for v in vs]
    if len(ports):
        values['service'] = {
            'ports': [_parse_port(p) for p in ports]
        }
    if len(ingress):
        values['ingress'] = {
            'rules': [_parse_ingress(i) for i in ingress],
            'tls': bool(ingress_tls),
            'tlsClusterIssuer': ingress_tls if type(ingress_tls) == 'string' else 'letsencrypt-prod',
            'ingressClass': ingress_class if type(ingress_class) == 'string' else 'nginx',
            'annotations': ingress_config
        }
    if len(labels):
        values['labels'] = labels
    if len(annotations):
        values['annotations'] = annotations
    if registry_secret:
        values['pullSecrets'] = [registry_secret]

    if build:
        kubectl_build(
            ref=image,
            context=context,
            dockerfile=dockerfile,
            dockerfile_contents=dockerfile_contents,
            registry_secret=registry_secret,
            build_args=build_args,
            secrets=build_secrets,
            labels=build_labels,
            extra_tags=build_tags,
            flags=build_flags
        )

    yaml = helm_template(
        name=name,
        values_contents=values,
        namespace=namespace,
        version=deploy_version,
        values=deploy_values,
        set=deploy_set,
        flags=deploy_flags,
        chart='component-chart',
        repo='https://charts.devspace.sh',
        api_versions=['networking.k8s.io/v1/Ingress'],
        kube_version='1.22.7',
    )
    if deploy:
        k8s_yaml(yaml, allow_duplicates=allow_duplicates)
    return yaml
