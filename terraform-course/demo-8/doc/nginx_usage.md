## resources
```bash
www.nginx.org
www.nginx.com
```
## /etc/nginx/nginx.conf
* uri match
```nginx
# check static API key
if ( $arg_apikey != 1234 ) {
  return 401 "Incorrect API key";
}
# preferential match
location ^~ /Greet2 {
  return 200 'greetings PREFERENTIAL';
}
# exact match
location = /greet {
  return 200 'greetings EXACT';
}
# regex match
location ~ /greet[0-9] {
  return 200 'greetings REGEX';
}
# regex match
location ~* /greet[0-9] {
  return 200 'greetings CASE INCENSITIVE';
}
```

* nginx build-in variables
* self-defined variables
```nginx
set $weekend 'No'; # try variables
if ( $date_local ~ 'Saturday|Sunday' ) {
  set $weekend 'Yes';
}
location = /is_weekend {
  # return 200 "$host\n$uri\n$args";
  return 200 $weekend;
}
```
* redirect
```nginx
location = /logo {
  return 307 /thumb.png;
}
```
* rewrite
```nginx
rewrite ^/user/\w+ /greet;
location /greet {
  return 200 "Hello User";
}
rewrite ^/user/(\w+) /greet/$1;
location /greet {
  return 200 "Hello User";
}
location = /greet/john {
  return 200 "Hello John";
}
```
* try files and named locations
* php backend, worker process
```bash
nginx -t # check syntax in nginx.conf
apt-get update
apt-get install php-fpm # install latest php backend, already configured as systemd service
systemctl list-units | grep php # verify installation
systemctl status php7.0-fpm # verify service of php7.0-fpm

nproc # check cpu cores
lscpu # check cpu information
ulimit -n # check maximum concurrent connections per core
ls -l /var/run/n* # check process file
```
```nginx
pid /var/run/new_nginx.pid # change default process id file name
worker_processes 2; #corespond to number of cpu cores
worker_processes auto; #spin one worker for each cpu core
events {
  worker_connections 1024; #maximum connections per worker process
  worker_connections auto; #
}
```
* buffers and timeouts
* add dynamic modules


## logs
```bash
/var/log/nginx/access.log
/var/log/nginx/error.log
```
```nginx
location = /secure {
  access_log /var/log/nginx/secure.access.log;
  # access_log off;
  return 200 "Hello from secure";
}
```
## enable http2
* add dynamic module http_v2
```bash
cd nginx-1.19.1
nginx -V # view installed modules
./configure --help | less # view available modules
./configue --help | grep http_v2 # view http2 module
./configue <paste current flags> --with-http_v2_module
make
make install
systemctl restart nginx
systemctl status nginx
```
* generate self-signed ssl certifiate for testing
```bash
mkdir /etc/nginx/ssl
openssl req -x509 -days 10 -nodes -newkey rsa:2048 \
-keyout /etc/nginx/ssl/self.key -out /etc/nginx/ssl/self.crt
```
```nginx
server {
  listen 443 ssl http2;
  ssl_certificate /etc/nginx/ssl/self.crt
  ssl_certificate_key /etc/nginx/ssl/self.key
}
```
## performance
* header caching
```nginx
location = /thumb.png {
  add_header my_header "hello world";
  add_header Cache_Control public;
  add_header Pragma public;
  add_header Vary Accept-Encoding;
  add_header Expires 1M;
```
