dotfile_config = """
location ~ /\\. {
  deny all;
  access_log           off;
  log_not_found        off;
  return               404;
}
"""

cache_config = """
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

try_file_config = """
location / {
  try_files \\$uri \\$uri/ /;
}
"""

nginx_config = """
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

dockerfile = """
FROM nginx:alpine
RUN cat > /etc/nginx/nginx.conf <<EOF
{nginx_config}
EOF
"""


def docker_nginx(dotfile=True,
                 cache=True,
                 try_file=True):
    config = nginx_config
    if dotfile:
        config = config.replace('{dotfile_config}', dotfile_config)
    else:
        config = config.replace('{dotfile_config}', '')
    if cache:
        config = config.replace('{cache_config}', cache_config)
    else:
        config = config.replace('{cache_config}', '')
    if try_file:
        config = config.replace('{try_file_config}', try_file_config)
    else:
        config = config.replace('{try_file_config}', '')
    return dockerfile.replace('{nginx_config}', config)
