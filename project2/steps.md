## install software
```bash
sudo su
apt-get update

export DEBIAN_FRONTEND=noninteractive
apt-get -yq dist-upgrade

apt-get install mysql-server -y # install mysql-server first

apt-get install nginx php7.0-mysql php7.0-fpm monit -y
# apt-cache search php | grep mysql
# apt list | grep php7.0-mysql
```
## config nginx
* backup original file
```bash
cd /etc/nginx
mv nginx.conf nginx.conf.ORIG
```
* copy over new file to /tmp/nginx.conf
```bash
sudo mv /tmp/nginx.conf /etc/nginx/nginx.conf
```
* create cache directory
```bash
mkdir -p /usr/share/nginx/cache/fcgi
```
* reload nginx
```bash
systemctl reload nginx
```
## config php-interpreter
* install php extensions for wordpress
```bash
apt-get install php-json php-xmlrpc php-curl php-gd php-xml php-mbstring -y
```
* ensure that directory for php-fpm sockets exists
```bash
mkdir /run/php-fpm

```
* backup php config file
```bash
mv /etc/php/7.0/fpm/php-fpm.conf /etc/php/7.0/fpm/php-fpm.conf.ORIG
```
* copy over new file to /tmp/php-fpm.conf
```bash
mv /tmp/php-fpm.conf /etc/php/7.0/fpm/php-fpm.conf
```
* backup www.conf
```bash
mv /etc/php/7.0/fpm/pool.d/www.conf /etc/php/7.0/fpm/pool.d/www.conf.ORIG
```
* copy over new file to /tmp/www.conf
```bash
mv /tmp/www.conf /etc/php/7.0/fpm/pool.d/www.conf
```
* backup php.ini
```bash
mv /etc/php/7.0/fpm/php.ini /etc/php/7.0/fpm/php.ini.ORIG
```
* copy over new file to /tmp/php.ini
```bash
mv /tmp/php.ini /etc/php/7.0/fpm/php.ini
```
## config database
* run mysql_secure_installation script, set root password
```bash
/usr/bin/mysql_secure_installation
systemctl restart mysql
```

## setup wordpress site
* create user for the site
```bash
useradd rfexpert
cd /home/rfexpert
chown rfexpert:rfexpert .
mkdir -p /home/rfexpert/logs
```
* Create nginx vhost config file
* copy over new file to /tmp/rfexpert.conf
```bash
mv /tmp/rfexpert.conf /etc/nginx/conf.d/rfexpert.conf
rm /etc/nginx/sites-enabled/default
```
* Create php-fpm vhost pool config file
* copy over new file to /tmp/rfexpert1.conf
```bash
mv /tmp/rfexpert1.conf /etc/php/7.0/fpm/pool.d/rfexpert1.conf
rm /etc/php/7.0/fpm/pool.d/www.conf
touch /home/rfexpert/logs/phpfpm_error.log
```
* create site database + db user
```bash
mysql -u root -p'***'
```
```mysql
CREATE DATABASE rfexpert;
CREATE USER 'rfexpert'@'localhost' IDENTIFIED BY 'random79561';
GRANT ALL PRIVILEGES ON rfexpert.* TO rfexpert@localhost;
FLUSH PRIVILEGES;
```
* install wordpress
```bash
su - rfexpert
cd
wget https://en-au.wordpress.org/latest-en_AU.tar.gz
tar zxf latest-en_AU.tar.gz
rm latest-en_AU.tar.gz
mv wordpress public_html
exit # become root again
cd /home/rfexpert/public_html
chown -R rfexpert:www-data .
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
```
* restart service
```bash
systemctl restart php7.0-fpm
systemctl restart nginx
chmod 640 /home/rfexpert/public_html/wp-config-sample.php
```
