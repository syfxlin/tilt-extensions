import os.path

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
    index                  {index};

    {dotfile_config}
    {cache_config}
    {try_file_config}

    include /etc/nginx/conf.d/*-server.conf;
  }}
  include /etc/nginx/conf.d/*-http.conf;
}}
"""

copy_nginx_config_tpl = """
COPY --chown=nginx:nginx ./.tilt/nginx /etc/nginx/conf.d
"""

dockerfile_tpl = """
FROM nginx:{version}

RUN cat > /etc/nginx/nginx.conf <<EOF
{nginx_config}
EOF

{copy_nginx_config}

RUN rm -f /usr/share/nginx/html/*
COPY --chown=nginx:nginx {root} /usr/share/nginx/html

{inject}
"""


def nginx_template(
    version='alpine',       # type: str
    root='public',          # type: str
    index='index.html',     # type: str
    dotfile=True,           # type: bool
    cache=True,             # type: bool
    try_file=True,          # type: bool
    inject=[]               # type: list[str]
):                          # type: (...) -> str
    nginx_config = nginx_config_tpl.format(
        index=index,
        dotfile_config=dotfile_config_tpl if dotfile else '',
        cache_config=cache_config_tpl if cache else '',
        try_file_config=try_file_config_tpl if try_file else ''
    )
    dockerfile = dockerfile_tpl.format(
        version=version,
        root=root,
        nginx_config=nginx_config,
        copy_nginx_config=copy_nginx_config_tpl if os.path.exists('./.tilt/nginx') else '',
        inject='\n'.join(inject)
    )
    return dockerfile
