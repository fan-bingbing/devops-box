## COPY vs ADD
* COPY can only copy local file or directory to container image
* ADD support URL source
* ADD support copy compressed file to container image and decompress that file automatically
* using ADD fetching resource from remote URL is discouraged, you should use
curl or wget instead. that way takes less layer when building image. 
```dockerfile
ADD file.tar.gz /tmp
```
## EXPOSE
* informs docker/image user that container listens on particular port at runtime
* it does not publish the port 
```dockerfile
EXPOSE 80
```
## HEALTHCHECK and options(default values)
* instruction on how to test if application is healthy
```bash
docker run -dt --name tmp2 --health-cmd "curl -f http://localhost" --health-interval=5s --health-retries=1 busybox sh
```
```dockerfile
HEALTHCHECK --intervals=5s CMD ping -c google.com
```
## CMD and ENTRYPOINT
* CMD can be overwritten 
```dockerfile
FROM busybox
CMD ["sh"]
```
```bash
docker container run -dt --name mybox mybox ping -c 10 google.com # overwrite CMD
```
* ENTRYPOINT can NOT be overwritten, but it can be appended
```dockerfile
FROM busybox
ENTRYPOINT ["/bin/ping"]
```
```bash
docker container run -dt --name mybox mybox -c 10 google.com # append ENTRYPOINT
```
## WORKDIR
* WORKDIR can be used multiple times
* it sets working directory for any RUN,CMD,ENTRYPOINT,COPY,ADD instructions that follow it
```dockerfile
FROM busybox
RUN mkdir /root/demo
WORKDIR /root/demo
RUN touch file01.txt
CMD ["/bin/sh"]
```
## ENV
* declare key value pair, key will be replaced with value 
```dockerfile
FROM busybox
ENV NGINX 1.2
RUN touch web-$NGINX.txt
CMD ["/bin/sh"]
```
```bash
docker run -dt --name env01 --env USER=user busybox sh
```




