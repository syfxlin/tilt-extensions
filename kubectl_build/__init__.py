import api.shlex as shlex
from api import *


def kubectl_build(ref,
                  context='.',
                  dockerfile=None,
                  dockerfile_contents=None,
                  namespace=None,
                  registry_secret=None,
                  pull=True,
                  push=True,
                  # values
                  build_args={},
                  secrets=[],
                  labels={},
                  extra_tags=[],
                  # extra args
                  cache_from=[],
                  cache_to=[],
                  builder=None,
                  skip_tls_verify=False,
                  target=None,
                  user=None,
                  token=None,
                  ssh=[],
                  extra_args=[],
                  # custom_build args
                  live_update=[],
                  match_in_env_vars=False,
                  ignore=[],
                  entrypoint=[]):
    # validate
    if dockerfile_contents != None and dockerfile != None:
        fail('Cannot specify both dockerfile and dockerfile_contents keyword arguments')

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

    # extra_args
    command += extra_args

    if dockerfile != None:
        dockerfile_path = dockerfile
    elif dockerfile_contents != None:
        dockerfile_path = '-'
    else:
        dockerfile_path = context + '/Dockerfile'
    command += ['--file', dockerfile_path]

    command = [shlex.quote(c) for c in command]
    command += ['-t', '$EXPECTED_REF']
    command += [shlex.quote(context)]
    command = ' '.join(command)

    deps = [context]
    if dockerfile_path != '-':
        deps += [dockerfile_path]
    else:
        command = 'echo {} | '.format(shlex.quote(dockerfile_contents)) + command

    custom_build(ref=ref,
                 command=command,
                 deps=deps,
                 live_update=live_update,
                 match_in_env_vars=match_in_env_vars,
                 ignore=ignore,
                 entrypoint=entrypoint,
                 disable_push=True,
                 skips_local_docker=True)
