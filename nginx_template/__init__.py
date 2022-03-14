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

events {
  worker_connections  1024;
}

include /etc/nginx/conf.d/*-root.conf;

http {
  server_tokens      off;
  include            /etc/nginx/mime.types;
  default_type       application/octet-stream;

  keepalive_timeout  65;
  sendfile           on;
  tcp_nopush         on;
  port_in_redirect   off;

  server {
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
  }
  include /etc/nginx/conf.d/*-http.conf;
}
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
"""


def replace_tpl(
        content,        # type: str
        values={}       # type: dict[str, str | tuple[bool, str] | tuple[bool, str, str]] | list[bool, str] | list[bool, str, str]
):                      # type: (...) -> str
    for k, v in values.items():
        key = '{' + k + '}'
        if (type(v) == 'tuple' or type(v) == 'list') and len(v) >= 2:
            if v[0]:
                value = str(v[1])
            elif len(v) >= 3 and not v[0]:
                value = str(v[2])
            else:
                value = ''
        else:
            value = str(v)
        content = content.replace(key, value)
    return content


def nginx_template(
        version='alpine',       # type: str
        root='./public',        # type: str
        index='index.html',     # type: str
        dotfile=True,           # type: bool
        cache=True,             # type: bool
        try_file=True,          # type: bool
        inject=[]               # type: list[str]
):                              # type: (...) -> str
    nginx_config = replace_tpl(nginx_config_tpl, {
        'index': index,
        'dotfile_config': [dotfile, dotfile_config_tpl],
        'cache_config': [cache, cache_config_tpl],
        'try_file_config': [try_file, try_file_config_tpl]
    })
    dockerfile = replace_tpl(dockerfile_tpl, {
        'version': version,
        'root': root,
        'nginx_config': nginx_config,
        'copy_nginx_config': [os.path.exists('./.tilt/nginx'), copy_nginx_config_tpl]
    })
    dockerfile += '\n'.join(inject)
    return dockerfile
