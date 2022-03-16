from write_file import *

allow_k8s_contexts(k8s_context())
load('../Tiltfile', 'write_file')

path = write_file('123')

print(path)
print(local(command='cat {}'.format(path), command_bat='cat {}'.format(path)))
