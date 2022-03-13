from api import *

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
    index                  index.html;

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
FROM nginx:alpine

RUN cat > /etc/nginx/nginx.conf <<EOF
{nginx_config}
EOF

{copy_nginx_config}

RUN rm -f /usr/share/nginx/html/*
COPY --chown=nginx:nginx {root} /usr/share/nginx/html
"""


def replace_tpl(content,
                name,
                tpl,
                condition=True):
    name = '{' + name + '}'
    if condition:
        return content.replace(name, tpl)
    else:
        return content.replace(name, '')


def docker_nginx(root='./public',
                 dotfile=True,
                 cache=True,
                 try_file=True):
    nginx_config = nginx_config_tpl
    dockerfile = dockerfile_tpl

    nginx_config = replace_tpl(nginx_config, 'dotfile_config', dotfile_config_tpl, dotfile)
    nginx_config = replace_tpl(nginx_config, 'cache_config', cache_config_tpl, cache)
    nginx_config = replace_tpl(nginx_config, 'try_file_config', try_file_config_tpl, try_file)

    dockerfile = replace_tpl(dockerfile, 'root', root)
    dockerfile = replace_tpl(dockerfile, 'nginx_config', nginx_config)
    dockerfile = replace_tpl(dockerfile, 'copy_nginx_config', copy_nginx_config_tpl, len(listdir('./.tilt/nginx')) > 0)

    return dockerfile
