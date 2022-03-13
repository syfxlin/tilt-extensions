from api import *
import os.path


def pull_secret(name,
                namespace=None,
                from_file=None,
                from_env=None,
                from_raw=None):
    if from_file != None and from_env != None and from_raw != None:
        fail('Cannot specify both from_file and from_env keyword arguments')

    command = ['kubectl', 'create', 'secret', 'generic', name]
    objects = [name, 'secret']
    home = os.environ['HOME']

    if from_file != None:
        command += ['--from-file', '.dockerconfigjson=' + from_file]
    elif from_env != None:
        command += ['--from-literal', '.dockerconfigjson=$' + from_env]
    elif from_raw != None:
        command += ['--from-literal', '.dockerconfigjson=' + from_raw]
    elif os.path.exists(os.path.join(home, '.docker/config.json')):
        command += ['--from-file', '.dockerconfigjson=' + os.path.join(home, '.docker/config.json')]
    else:
        command += ['--from-literal', '$DOCKER_CONFIG']

    command += ['--type=kubernetes.io/dockerconfigjson']
    command += ['--output=yaml']
    command += ['--dry-run=client']

    if namespace:
        command += ['--namespace', namespace]
        objects += [namespace]

    k8s_yaml(local(command, quiet=True, echo_off=True))
    k8s_resource(new_name=name, objects=[':'.join(objects)])
