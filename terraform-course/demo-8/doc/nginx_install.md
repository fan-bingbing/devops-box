## installing with a package manager
```bash
# quick and easy
# limited install options
# no support for additional modules
# only suitable for testing and development
apt-get update
apt-get intall nginx
ps aux | grep nginx # verity nginx is running
ls -l /etc/nginx # config files location

#switch to centos, revolve warning: remote host identification has changed
ssh-keygen -R target_hostname(or ip)
```
## building nginx from source & add modules
```bash
apt-get update
# go to nginx.org, download page, copy download mainline version link
wget ...
tar -zxvf nginx-***.tar.gz
cd nginx-1.19.1

# configuring source code for the build, c compiler not found
./configure
# install build tools
apt-get install build-essential
# install PCRE library and other libraries, run configure again
apt-get install libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev
./configure
# reconfigure the source and set flags, refer to nginx.org build from source docs
./configure --sbin-path=/usr/bin/nginx --conf-path=/etc/nginx/nginx.conf
--error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log
--with-pcre --pid-path=/var/run/nginx.pid --with-http_ssl_module
# compile the source
make
# install the compile source
make install
# check config file directory
ls -l /etc/nginx
# verify nginx version
nginx -V
# run nginx
nginx
# verify
ps aux | grep nginx
# nginx tools
nginx -h
# stop nginx is important before doing next steps
nginx -s stop

# add systemd service, download nginx init script from nginx.com for systemd

nano /lib/systemd/system/nginx.service
# edit file path
PIDFile=/var/run/nginx.pid,
ExecStartPre=/usr/bin/nginx -t,
ExecStart=/usr/bin/nginx

# verity systemctl cammands
systemctl start nginx
systemctl stop nginx
systemctl enable nginx

```
