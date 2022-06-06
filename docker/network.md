## network drivers available
bridge, host...
```bash
ip a # verify interface docker0
docker network ls # default bridge
docker network inspect bridge
docker network inspect host
```

## bridge network
docker0 (172.17.0.1) act as default gateway on host
container by default gets created in bridge network (172.17.0.0/16)
containers in the network are able to communicate each other
```bash
docker container inspect myhost # find out network type, ip address of the container
docker container run -dt --name web -P nginx # publish all expposed ports to random ports of the host
```
## user-defined bridge network
```bash
yum whatprovides brctl # find out bridge-utils provide brctl command
yum install bridge-utils

# one of the features of user-defined bridge network is providing DNS out of box
# whereas default bridge network don't provide DNS

# user-defined bridge provide DNS automatically, can ping using container name
docker network create --driver bridge mybridge
docker network ls
docker network inspect

```

# host network
host network removes isolation between host and containers
for instance automatic port mapping, 80:80
```bash
docker container run -dt --name myhost --network host ubuntu # launch ubuntu in host network

```

## None network
disable networking stack on containers, no ips, no access to external network
```bash
docker container run -dt --name mynone --network none ubuntu
```
