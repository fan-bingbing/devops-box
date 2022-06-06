## linux namespaces
a linux kernel feature that creates first form of isolation
each aspect of container runs in a separate namespace and its access limited to that namespace
such as: PID namespace, UTS namespace
```bash
docker container run -dt --name mybusybox busybox sh
ps -ef # see lots of PID running on host 
docker container exec -it mybusybox sh
ps -ef # only show limited PID in container, PID on host is not accessable   

unshare -fp --mount-proc /bin/bash # create a PID namespace in linux
ps -ef 
exit
```

## control groups (cgroups)
a linux kernel feature that limits, account for resource usage(CPU, memory, diskI/O...)
ensure that each container gets its fair amount of memory, CPU, diskI/O, so a single container
cannnot bring the sytem down by exhausting one of those reources
```bash

free -m # check available memory on host
docker info # check total number of CPU and memory that docker has 
docker container run -dt --name mybusybox -m 256m busybox sh
docker container run -dt --name mybusybox --cpus=1.5 busybox sh
docker container run -dt --name mybusybox --cpuset-cpu=1,2 busybox sh # allocate second,third CPU to container 

docker container exec -it mybusybox sh
free -m # check available memory in container, you still see memory value on host 
top # check available memory in container, you still see memory value on host

cat /sys/fs/cgroup/memory/memory.limit_in_bytes # you can see 256M available in container  
```

## docker content trust (DCT)
only repositories signed with a user-specified root key can be pulled and run. 

```bash
docker trust inspect nginx # check trusted signers
export DOCKER_CONTENT_TRUST=1 # enable DCT
```

## linux capabilities
several types of capabilities which linux provide to have granular access at the application level.
```bash
docker container run -dt --name cap-demo amazonlinux
docker container exec -it cap-demo bash
whoami # verity logged as root
touch test.txt
yum whatprovides chattr # found that it's part of e2fsprogs
yum install e2fsprogs # chattr is used to set immutable bit of file
chattr +i test.txt # operation not permitted even though logged in as root

docker container run -dt --name cap-demo --cap-add LINUX_IMMUTABLE amazonlinux bash
# try chattr again it should work
# immtable bit prevents file from being accidentally modified or deleted
```
## privileged containers
by default docker container does not have many capabilities assigned to it.
running a privileged flag gives all capabilities to the container.
use case: run docker inside docker.
```bash
docker container run -dt --name priv-demo --privileged amazonlinux bash
docker container exec -it priv-demo bash
ls /dev # verify it has access to storage devices on host

```

## docker groups
```bash
nano /etc/group
# add non-previleged newuser in docker group
docker:x:993: newuser

usermod -aG docker newuser # prefer way adding newuser to docker group
```

