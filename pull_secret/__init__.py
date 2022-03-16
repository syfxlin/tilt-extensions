from api import *
import os.path


def pull_secret(
    name,               # type: str
    namespace='',       # type: str
    from_file='',       # type: str
    from_env='',        # type: str
    from_raw=''         # type: str
):                      # type: (...) -> None
    if from_file != '' and from_env != '' and from_raw != '':
        fail('Cannot specify both from_file and from_env keyword arguments')

    command = ['kubectl', 'create', 'secret', 'generic', name]
    home = os.environ['HOME']

    if from_file != '':
        command += ['--from-file', '.dockerconfigjson=' + from_file]
    elif from_env != '':
        command += ['--from-literal', '.dockerconfigjson=$' + from_env]
    elif from_raw != '':
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

    k8s_yaml(local(command, quiet=True, echo_off=True))
