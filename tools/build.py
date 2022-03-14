import os
import re

ignore = ['api', 'tools', '.git', '.idea']
root = os.getcwd()


def convert(path: str):
    if not os.path.isdir(d) or not os.path.exists(os.path.join(d, '__init__.py')):
        return
    src_path = os.path.join(path, '__init__.py')
    dist_path = os.path.join(path, 'Tiltfile')
    src_file = open(src_path, 'r')
    dist_file = open(dist_path, 'w')
    output = ''

    import_pattern = re.compile('^\s*(import|from)\s+')
    define_pattern = re.compile('^# define$')
    for line in src_file.readlines():
        if define_pattern.match(line):
            break
        if not import_pattern.match(line):
            output += line
    dist_file.write(output)


for d in os.listdir(root):
    if d not in ignore:
        convert(d)

        test = os.path.join(d, 'test')
        if os.path.exists(test) and os.path.isdir(test):
            convert(test)
