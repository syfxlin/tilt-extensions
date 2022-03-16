import os.path

pnpm_copy_tpl = """
COPY package.json pnpm-lock.yaml ./
"""

yarn_copy_tpl = """
COPY package.json yarn.lock ./
"""

npm_copy_tpl = """
COPY package*.json ./
"""

pnpm_install_tpl = """
RUN pnpm install --prod --frozen-lockfile
"""

yarn_install_tpl = """
RUN yarn install --production --frozen-lockfile && yarn cache clean
"""

npm_install_tpl = """
RUN npm ci --only=production && npm cache clean --force
"""

pnpm_build_tpl = """
RUN pnpm run build
"""

yarn_build_tpl = """
RUN yarn run build
"""

npm_build_tpl = """
RUN npm run build
"""

pnpm_start_tpl = """
CMD ["pnpm", "run", "start"]
"""

yarn_start_tpl = """
CMD ["yarn", "run", "start"]
"""

npm_start_tpl = """
CMD ["npm", "run", "start"]
"""

node_start_tpl = """
CMD ["node", "index.js"]
"""

dockerfile_tpl = """
FROM gplane/pnpm:{version}

WORKDIR /app

{pm_copy}
{inject_prepare}
{pm_install}

COPY . .

{inject}
{pm_start}

ENTRYPOINT ["docker-entrypoint.sh"]
"""

dotfile_config_tpl = """
location ~ /\\. {
  deny all;
  access_log           off;
  log_not_found        off;
  return               404;
}
"""

cache_config_tpl = """
location ~* \\.(?:css|js)$ {
  access_log           off;
  log_not_found        off;
  add_header           Cache-Control "no-cache, public, must-revalidate, proxy-revalidate";
}

location ~* \\.(?:jpg|jpeg|gif|png|ico|xml|webp|eot|woff|woff2|ttf|svg|otf)$ {
  access_log           off;
  log_not_found        off;
  expires              60m;
  add_header           Cache-Control "public";
}
"""

try_file_config_tpl = """
location / {
  try_files \\$uri \\$uri/ /;
}
"""

nginx_config_tpl = """
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {{
  worker_connections  1024;
}}

include /etc/nginx/conf.d/*-root.conf;

http {{
  server_tokens      off;
  include            /etc/nginx/mime.types;
  default_type       application/octet-stream;

  keepalive_timeout  65;
  sendfile           on;
  tcp_nopush         on;
  port_in_redirect   off;

  server {{
    listen 80;
    charset utf-8;
    server_name  _;

    real_ip_header         x-forwarded-for;
    set_real_ip_from       0.0.0.0/0;
    real_ip_recursive      on;

    root                   /usr/share/nginx/html;
    index                  {nginx_index};

    {nginx_dotfile_config}
    {nginx_cache_config}
    {nginx_try_file_config}

    include /etc/nginx/conf.d/*-server.conf;
  }}
  include /etc/nginx/conf.d/*-http.conf;
}}
"""

copy_nginx_config_tpl = """
COPY --chown=nginx:nginx ./.tilt/nginx /etc/nginx/conf.d
"""

dockerfile_static_tpl = """
FROM gplane/pnpm:{version} as builder

WORKDIR /app

{pm_copy}
{inject_prepare}
{pm_install}

COPY . .

{inject_prebuild}
{pm_build}
{inject}

FROM nginx:{nginx_version}

RUN cat > /etc/nginx/nginx.conf <<EOF
{nginx_config}
EOF

{copy_nginx_config}

RUN rm -f /usr/share/nginx/html/*
COPY --chown=nginx:nginx --from=builder /app/{nginx_root} /usr/share/nginx/html

{nginx_inject}
"""


def nodejs_template(
    version='alpine',           # type: str
    inject_prepare=[],          # type: list[str]
    inject=[],                  # type: list[str]
    cmd=[]                      # type: list[str]
):
    pm_copy = ''
    pm_install = ''
    pm_start = node_start_tpl
    if os.path.exists('./pnpm-lock.yaml'):
        pm_copy = pnpm_copy_tpl
        pm_install = pnpm_install_tpl
        pm_start = pnpm_start_tpl
    elif os.path.exists('./yarn.lock'):
        pm_copy = yarn_copy_tpl
        pm_install = yarn_install_tpl
        pm_start = yarn_start_tpl
    elif os.path.exists('./package.json'):
        pm_copy = npm_copy_tpl
        pm_install = npm_install_tpl
        pm_start = npm_start_tpl
    if len(cmd) > 0:
        pm_start = 'CMD ["{}"]'.format('", "'.join(cmd))
    dockerfile = dockerfile_tpl.format(
        version=version,
        pm_copy=pm_copy,
        inject_prepare='\n'.join(inject_prepare),
        pm_install=pm_install,
        pm_start=pm_start,
        inject='\n'.join(inject),
        cmd=cmd
    )
    return dockerfile


def nodejs_static_template(
    version='alpine',           # type: str
    inject_prepare=[],          # type: list[str]
    inject_prebuild=[],         # type: list[str]
    inject=[],                  # type: list[str]
    # nginx
    nginx_version='alpine',     # type: str
    nginx_root='./public',      # type: str
    nginx_index='index.html',   # type: str
    nginx_dotfile=True,         # type: bool
    nginx_cache=True,           # type: bool
    nginx_try_file=True,        # type: bool
    nginx_inject=[]             # type: list[str]
):
    pm_copy = ''
    pm_install = ''
    pm_build = ''
    if os.path.exists('./pnpm-lock.yaml'):
        pm_copy = pnpm_copy_tpl
        pm_install = pnpm_install_tpl
        pm_build = pnpm_build_tpl
    elif os.path.exists('./yarn.lock'):
        pm_copy = yarn_copy_tpl
        pm_install = yarn_install_tpl
        pm_build = yarn_build_tpl
    elif os.path.exists('./package.json'):
        pm_copy = npm_copy_tpl
        pm_install = npm_install_tpl
        pm_build = npm_build_tpl
    nginx_config = nginx_config_tpl.format(
        nginx_index=nginx_index,
        nginx_dotfile_config=dotfile_config_tpl if nginx_dotfile else '',
        nginx_cache_config=cache_config_tpl if nginx_cache else '',
        nginx_try_file_config=try_file_config_tpl if nginx_try_file else ''
    )
    dockerfile = dockerfile_static_tpl.format(
        version=version,
        pm_copy=pm_copy,
        inject_prepare='\n'.join(inject_prepare),
        pm_install=pm_install,
        inject_prebuild='\n'.join(inject_prebuild),
        pm_build=pm_build,
        inject='\n'.join(inject),
        # nginx
        nginx_version=nginx_version,
        nginx_config=nginx_config,
        copy_nginx_config=copy_nginx_config_tpl if os.path.exists('./.tilt/nginx') else '',
        nginx_root=nginx_root,
        nginx_inject='\n'.join(nginx_inject)
    )
    return dockerfile
