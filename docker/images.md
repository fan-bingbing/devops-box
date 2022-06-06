## searching images
search dockerhub by default
```bash
docker search --limit=5 alpine
docker search --filter is-automated=true --filter stars=20 alpine
```
## tag image 
```bash
docker build -t demo:v1 . # tag image when build 
docker tag image-id demo:v2 # tag existing image
docker images # verify tagging 
```
## docker commit
```bash
# save changes for a running container to new image
docker container commit busybox busybox-modified
docker container diff busybox-modified

# change busybox image and save in a new image
docker container commit --change='CMD ["ash"]' busybox 
```
## image layers
* one instruction generates one layer 
* minimize number of instructions to reduce number of layers/size of image
```bash
docker image history ubuntu # inspect layers of image ubuntu 
```
## docker image child command
```bash
docker image --help
docker image inspect nginx --format='{{.ContainerConfig.Hostname}}' # filtering info 
docker image prune # delete dangling images without tags and are not associate with any container 
docker image prune -a # delete images that are not associate with any container 
```
## flattening images
```bash
docker container run -dt --name myubuntu ubuntu
docker export myubuntu > myubuntudemo.tar # for reducing image size 
cat myubuntudemo.tar | docker import - myubuntu:latest # generate one layer image
docker image history myubuntu # verify one layer
```
## docker registry
```bash
docker container run -d -p 5000:5000 --restart always --name registry registry:2 # pull and run docker registry locally
docker image tag ubuntu:latest localhost:5000/myubuntu:1 # retag ubuntu image 
docker image push localhost:5000/myubuntu:1 # push to local docker registry
docker image pull localhost:5000/myubuntu:1 # pull image from local docker registry
```
## dockerhub 
```bash 
docker login # supply username password
docker tag busybox:latest fanbingbing/mybusybox:1
docker push fanbingbing/mybusybox:1
docker pull fanbingbing/mybusybox:1
docker logout
cat ~/.docker/config.json # explore registry credentials
```
## filter images
```bash
docker search --help
docker search nginx --limit 5 # search images in dockerhub
```
## move images
```bash
docker save myapp > myapp.tar # .tar file can be moved around 
docker load < myapp.tar
```
## using cache
if the cache can't be used for a particular layer, all subsequent layers won't be loaded from the cache.
