from kubectl_build import *
from pull_secret import *

load('../Tiltfile', 'pull_secret')
load('../../kubectl_build/Tiltfile', 'kubectl_build')

allow_k8s_contexts(['contabo'])

k8s_yaml('deployment.yml')
pull_secret('tilt-cr-ixk-me')
kubectl_build('cr.ixk.me/syfxlin/demo', registry_secret='tilt-cr-ixk-me')
k8s_resource(workload='demo', port_forwards='8080:80')
