## docker storage drivers
```bash
docker info # storage driver default to be overlay2
ls -al /var/lib/docker # overlay2 directory exist

cd /var/lib/docker/overlay2
du -sh * # verify different layer size

cd /var/lib/docker/overlay2/l # symbolic links to layers
```
## block storage VS object storage
object storage has no blocks, object is saved as file with meta data, for instance: s3
object storage supprt HTTP(S) interface, accessable from browser

most of linux file system are block storage, every block has an address, no meta data.
```bash
blockdev -getbsz /dev/sda # show block size of sda
lsblk # list block storage device

```
## change of storage drivers
after change of storage driver, all previous container are no longer accessible
whenever possible, overlay2 is the recommended storage driver
image layers: R/O
container layer: R/W, depends on container's existence
```bash
docker info
systemctl stop docker
cd /etc/docker

nano daemon.json
{
    "storage driver": "aufs"
}

systemctl start docker
```
## volumes VS bind mounts
volumes -> /var/lib/docker/volumes, persistent
bind mounts -> host filesystem, persistent
tmpfs mount -> memory, not persistent
```bash
docker volume ls
docker volume create myvolume
docker container run -dt --name busybox -v myvolume:/etc busybox sh
docker volume inspect myvolume
docker volume rm myvolume

mkdir /index
echo this is bindmount file > /index/index.html
docker container run -dt --name nginx -v /index:/usr/share/nginx/html nginx
# bindmount can be set to read only, prevent from changes of file on host
```

## remove volumes when container exit
```bash
# remove container and volumes when container is delteted
docker container run --rm -dt --name container01 -v /testvolume busybox ping -c10 google.com

```
## logging drivers
json-file is the default logging driver
docker logs command is not available for drivers other than json-file and journald
```bash
docker container run -d --name mybusybox busybox ping google.com
docker logs mybusybox # check stdout and stderr of container mybusybox
docker container inspect mybusybox | grep "LogPath" # find out log path
```
