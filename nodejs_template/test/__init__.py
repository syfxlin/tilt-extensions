from kubectl_build import *
from nodejs_template import *
from pull_secret import *

load('../../kubectl_build/Tiltfile', 'kubectl_build')
load('../../pull_secret/Tiltfile', 'pull_secret')
load('../Tiltfile', 'nodejs_static_template')

allow_k8s_contexts(k8s_context())

k8s_yaml('deployment.yml')
pull_secret('tilt-cr-ixk-me')
kubectl_build('cr.ixk.me/syfxlin/demo', dockerfile_contents=nodejs_static_template(), registry_secret='tilt-cr-ixk-me')
k8s_resource(workload='demo', port_forwards='8080:80')
