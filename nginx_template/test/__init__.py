from kubectl_build import *
from nginx_template import *
from pull_secret import *

load('../../kubectl_build/Tiltfile', 'kubectl_build')
load('../Tiltfile', 'nginx_template')

os.putenv('TILT_DIR', 'C:/Users/syfxl/AppData/Local/tilt-dev')

allow_k8s_contexts(k8s_context())

k8s_yaml('deployment.yml')
kubectl_build('cr.ixk.me/syfxlin/demo', dockerfile_contents=nginx_template(), registry_secret='cr-ixk-me')
k8s_resource(workload='demo', port_forwards='8080:80')
