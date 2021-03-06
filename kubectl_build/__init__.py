from api import shlex
from write_file import *

load('../write_file/Tiltfile', 'write_file')


def kubectl_build(
    ref,                        # type: str
    context='.',                # type: str
    dockerfile='',              # type: str
    dockerfile_contents='',     # type: str
    namespace='kube-system',    # type: str
    registry_secret='',         # type: str
    pull=True,                  # type: bool
    push=True,                  # type: bool
    # values
    build_args={},              # type: dict[str, str]
    secrets=[],                 # type: list[str]
    labels={},                  # type: dict[str, str]
    extra_tags=[],              # type: list[str]
    # extra args
    cache_from=[],              # type: list[str]
    cache_to=[],                # type: list[str]
    builder='',                 # type: str
    skip_tls_verify=False,      # type: bool
    target='',                  # type: str
    user='',                    # type: str
    token='',                   # type: str
    ssh=[],                     # type: list[str]
    flags=[],                   # type: list[str]
    # custom_build args
    live_update=[],             # type: list[LiveUpdateStep]
    match_in_env_vars=False,    # type: bool
    ignore=[],                  # type: list[str]
    entrypoint=[]               # type: list[str]
):                              # type: (...) -> None
    # validate
    if dockerfile_contents != '' and dockerfile != '':
        fail('Cannot specify both dockerfile and dockerfile_contents keyword arguments')

    # deps
    deps = [context]
    # command
    command = ['kubectl', 'build']
    # context
    command += ['--context', k8s_context()]

    # namespace
    if namespace:
        command += ['--namespace', namespace]
    # registry_secret
    if registry_secret:
        command += ['--registry-secret', registry_secret]
    # pull & push
    if pull:
        command += ['--pull']
    if push:
        command += ['--push']

    # build_args & secrets & labels & extra_tags
    for name, value in build_args.items():
        command += ['--build-arg', name + '=' + value]
    for name, value in labels.items():
        command += ['--label', name + '=' + value]
    for value in secrets:
        command += ['--secret', value]
    for value in extra_tags:
        command += ['--tag', value]

    # cache_from & cache_to
    for value in cache_from:
        command += ['--cache-from', value]
    for value in cache_to:
        command += ['--cache-to', value]
    # builder
    if builder:
        command += ['--builder', builder]
    # skip_tls_verify
    if skip_tls_verify:
        command += ['--insecure-skip-tls-verify']
    # target
    if target:
        command += ['--target', target]
    # user
    if user:
        command += ['--user', user]
    # token
    if token:
        command += ['--token', token]
    for value in ssh:
        command += ['--ssh', value]

    # flags
    command += flags

    if dockerfile != '':
        dockerfile_path = dockerfile
        deps += [dockerfile_path]
    elif dockerfile_contents != '':
        dockerfile_path = write_file(dockerfile_contents)
    else:
        dockerfile_path = context + '/Dockerfile'
        deps += [dockerfile_path]
    command += ['--file', dockerfile_path]

    command = [shlex.quote(c) for c in command]
    command += ['-t', '$EXPECTED_REF']
    command += [shlex.quote(context)]
    command = ' '.join(command)

    custom_build(
        ref=ref,
        command=command,
        command_bat='powershell.exe -NoProfile -Command {}'.format(
            command.replace('$EXPECTED_REF', '$env:EXPECTED_REF')
        ),
        deps=deps,
        live_update=live_update,
        match_in_env_vars=match_in_env_vars,
        ignore=ignore,
        entrypoint=entrypoint,
        disable_push=True,
        skips_local_docker=True
    )
