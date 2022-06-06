# Networking
## 1. switching and routing
```bash
hostname
uname -n
hostname -f # fully qualified domain name
echo 'webprod01' > /etc/hostname # change host name
ls /etc/services # map port to services


ip link # list or modify interfaces on host
ip addr # check ip address assigned to interfaces
ip addr add 192.168.1.10/24 dev eth0 # set ip address on interfaces
ip link set eth0 up
ip route # view routing table or use route -n
ip route add 192.168.1.0/24 via 192.168.2.1 # add entries in routing table

echo ... >> /etc/network/interfaces # persist config over reboot
# newer ubuntu18.04, go to /etc/netplan configure yaml file accordingly
# in centOS, go to /etc/sysconfig/network-scripts configure ifcfg-eth* file accordingly

cat /proc/sys/net/ipv4/ip_forward # check value for ip_forwarding, 1 or 0
# this is necessary for configuring host acting as a router
cat /etc/sysctl.conf # net.ipv4.ip_forward = 1 make port forwarding persistent

arp
route # find out default gateway address
ping google.com
traceroute -n google.com #
tracepath -n google.com
netstat -tupln # list listening ports
tcpdump # packing sniffing

```
## 2. DNS
### dns record types
#### A web-server 192.168.1.1
#### AAAA web-server 2001:0db8:85a3:...
#### CNAME food.web-server eat.web-server, hungry.web-server

### /etc/hosts for local mapping
```bash
echo 192.168.1.11 db >> /etc/hosts
echo 192.168.1.11 www.google.com >> /etc/hosts
ping db # look for ip address in /etc/hosts
ssh db # look for ip address in /etc/hosts
curl http://www.google.com # look for ip address in /etc/hosts
```
### /etc/resolv.conf for remote dns server
```bash
echo nameserver 192.168.1.100 >> /etc/resolv.conf # set dns server address
echo namesever 8.8.8.8 # use google dns server
echo search google.com mycompany.com prod.mycompany.com >> /etc/resolv.conf
# make mail.mycompany.com, test.prod.mycompany.com available
nslookup www.google.com # ignore /etc/hosts file, query dns server only
dig www.google.com # the same as nslookup

cat /etc/nsswitch.conf # revise DNS resolution sequence
```
### coredns(dns setup tool) in kubernetes

## 3. docker networking
### network options in docker
```bash
docker run --network none nginx # no network access to containers
docker run --network host nginx # containers share network with host, no isolation
docker run --network bridge nginx # create internal private network for containers
docker run -p 8080:80 nginx # map host port 8080 to docker port 80
```

## 4. kubelet and pods networking
### kubelet create pods and invoke CNI to assign ip to pods
### CNI: standard network plugins for different container runtime
### check CNI(network setup tool) in kubernetes: weave
### schedule a pod on a node, check default gateway of the pod on this node
```bash
cd /etc/cni/net.d/weave.config # weave configuration file
ps aux | grep kubelet

https://www.weave.works/docs/net/latest/kubernetes/kube-addon/
```
## 5. kube-proxy and service networking
### kube-proxy assign ip to service (a virtual object across cluster)
```bash
kubectl logs kube-proxy-ft6n7 -n kube-system # check proxier type, iptables by default
kubectl get pods -o wide
kubectl get service
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep cluster-ip-range # check service ip range
iptables -L -t net | grep service-name # check ip forwarding from pods to services
```

## 6. dns in kubernetes
### fully qualified domain name
```bash
curl http://web-service # webservice in default namespace
curl http://web-service.apps # webservice in apps namespace
curl http://web-service.apps.svc.cluster.local # fully qualified service domain name
curl http://10-244-2-5.apps.pod.cluster.local # fully qualified pod domain name
```
### dns implementation: coredns
```bash
cat /etc/coredns/Corefile # coredns configuration file
kubectl get configmap -n kube-system # coredns configmap pass into config file
kubectl get svc -n kube-system # kube-dns service
cat /etc/resolv.conf # find nameserver record: ip of kube-dns
host web-service # find fully qualified domain name and ip address
host 10-244-2-5.default.pod.cluster.local # pod only works on fully qualified domain name
```
## 6. ingress: layer7 load balancer built in k8s cluster

### ingress controller(nginx), including following objects
#### a. Deployment: nginx-ingress-controller using special built nginx image
#### b. Configmap: nginx-configuration
#### c. Service: nginx-service(NodePort)
#### d. Serviceaccount: nginx-ingress-serviceaccount(Roles, ClusterRoles, RoleBindings)

### ingress resources(yaml files), including following objects
#### a. Ingress: mapping URLs to backends(services) through Rules(www.[xy.]abc.com) and Paths(www.abc.com/[xy])
```bash
kubectl create -f ingress_file.yaml
kubectl get ingress
kubectl describe ingress

minikube addons list
minikube addons enable ingress
kubectl get pod -n kube-system # verify nginx-ingress-controller pod runnig

```
