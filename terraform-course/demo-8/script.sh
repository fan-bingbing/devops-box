#!/bin/bash

# sleep until instance is ready
until [[ -f /var/lib/cloud/instance/boot-finished ]]; do
  sleep 1
done

apt-get update
# go to nginx.org, download page, copy download mainline version link
wget https://nginx.org/download/nginx-1.19.1.tar.gz
tar -zxvf nginx-1.19.1.tar.gz
cd nginx-1.19.1
# install build tools
apt-get install build-essential -y
# install PCRE library and other libraries, run configure again
apt-get install libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev python mysql-client -y
./configures
# reconfigure the source and set flags, refer to nginx.org build from source docs
./configure --sbin-path=/usr/bin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-pcre --pid-path=/var/run/nginx.pid --with-http_ssl_module
# compile the source
make
# install the compile source
make install
