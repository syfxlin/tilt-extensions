from deployment import *

load('../Tiltfile', 'deployment')

allow_k8s_contexts(k8s_context())

deployment(
    name='demo',
    image='cr.ixk.me/syfxlin/demo',
    registry_secret='cr-ixk-me',
    command=['test', 'run'],
    args=['--a', '--b'],
    env=[
        ['key1', 'value1'],
        ['key2', '@cm', 'cmName', 'cmKey'],
        ['key3', '@sec', 'secName', 'secKey'],
        ['key4', '@field', 'fieldPath'],
        ['key5', '@resource', 'resource']
    ],
    volumes=[
        ['volume1', '/volume1', '1Gi'],
        ['volume2', '/volume2', '@emptyDir'],
        ['volume3', '/volume3', '@cm', 'cmName'],
        ['volume4', '/volume4', '@sec', 'secName'],
        ['volume5', '/volume5', 'local-path', '1Gi'],
        ['volume5', '/volume5', 'local-path', '1Gi', '/123'],
    ],
    ports=[
        80,
        [443, 443],
        [8080, 8080, 'UDP']
    ],
    ingress=[
        'demo.ixk.me',
        ['demo1.ixk.me', '/path1'],
        ['demo2.ixk.me', '/path2', 'Prefix'],
        ['demo3.ixk.me', '/path3', 'Prefix', 8080]
    ],
    ingress_class='nginx',
    ingress_tls=True,
    ingress_config={
        'nginx.ingress.kubernetes.io/server-alias': 'www.ixk.me',
        'nginx.ingress.kubernetes.io/from-to-www-redirect': 'true'
    },
    labels={
        'app': 'demo'
    },
    annotations={
        'app': 'demo'
    }
)
