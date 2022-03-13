import os
import re

ignore = ['api', 'tools', '.git', '.idea']
root = os.getcwd()


def convert(path: str):
    src_path = os.path.join(path, '__init__.py')
    dist_path = os.path.join(path, 'Tiltfile')
    src_file = open(src_path, 'r')
    dist_file = open(dist_path, 'w')
    output = ''

    pattern = re.compile('^\s*(import|from)\s+')
    for line in src_file.readlines():
        if not pattern.match(line):
            output += line
    dist_file.write(output)


for d in os.listdir(root):
    if os.path.isdir(d) and os.path.exists(os.path.join(d, '__init__.py')) and d not in ignore:
        convert(d)
