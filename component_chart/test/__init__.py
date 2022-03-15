from component_chart import *
from kubectl_build import *
from pull_secret import *

load('../Tiltfile', 'component_chart')
load('../../kubectl_build/Tiltfile', 'kubectl_build')
load('../../pull_secret/Tiltfile', 'pull_secret')

allow_k8s_contexts(['contabo'])

values = """
containers:
  - name: demo
    image: cr.ixk.me/syfxlin/demo
service:
  ports:
    - name: http
      port: 80
pullSecrets:
  - tilt-cr-ixk-me
"""

component_chart(
    name='demo',
    values_contents=values
)

pull_secret('tilt-cr-ixk-me')
kubectl_build('cr.ixk.me/syfxlin/demo', registry_secret='tilt-cr-ixk-me')
k8s_resource(workload='demo', port_forwards='8080:80')
