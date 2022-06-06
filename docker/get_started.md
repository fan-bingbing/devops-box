## container identification
UUID
container ID, shorthand format
container name, if not specified, a random name will be generated
add label for filtering/selection using --label
container information resides in /var/lib/docker/containers
```bash
docker container run --name mynginx -d -p 80:80 nginx --label=abc.com=dev
docker ps
docker container inspect
docker container ls -a --filter label=abc.com=dev
```
## port binding
```bash
docker run --name mynginx -d -p 8000:80 nginx
docker ps
netstat -tupln # verify port 8000 is listening on host
```
## attach and detach mode
```bash
docker run --name mynginx -d -p 8000:80 nginx
```
## remove containers
```bash
docker container stop/rm $(docker container ls -aq) # stop/remove all containers
docker ps
docker container rm nginx # remove container
docker container prune -f # remove all stopped containers
```
## inject a process into running container, '-it' is important
```bash
docker run --name mynginx -d -p 8000:80 nginx
docker container exec -it nginx bash # get inside container nginx

# PID1 must be running
# -i gives interactive stdin, -t gives tty
docker container exec -it nginx netstat -tupln # run netstat from outside

ID=$(docker container run -dt ubuntu)
docker container exec -it $(ID) /bin/bash # get inside container nginx
ps aux
```
## default container command, and how to overwrite this command
whenever run a container, default container command run as PID1, defined in Dockerfile
```bash
docker container run -d nginx sleep 500
# sleep 500 repalced default command
# after 500s container will exit
```
## restart policy
when docker demon restart and when container exit for whatever reason,
how container restart (manually or automatically)
```bash
docker container run -d --restart unless-stopped nginx
```
## disk usage metrics for docker component
```bash
docker system df
docker system df -v # breakdown of disk usage per container
```
## delete container on exit
```bash
docker container run -d --rm --name mybox busybox ping -c10 google.com
docker logs mybox

```

## check logs
container logs resides in /var/lib/docker/containers/<container ID>/<container ID>-json.log
```bash
docker container logs mybox -t -f # timestamp, following logs
```
