# Trouble shoot
## 1. application failure
```bash
curl http://web-service-ip:node-port # check connectivity of web service

kubectl describe service web-service # check endpoint
kubectl get pods # check status of all pods
kubectl get pod web -o yaml # check service selector match pod label
kubectl get pod web # make sure pod web is in running state

kubectl describe pod web # check status of pod
kubectl logs web [--previous]

# check database service and pod as well

```
## 2. control plane failure
```bash
kubectl get nodes # check nodes status
kubectl get pods # check pods status
kubectl get pods -n kube-system # check control plan pods status
kubectl logs kube-apiserver-master -n kube-system
kubectl cluster-info # verify apiserver, kubeDNS endpoint

ls /etc/kubernetes/manifests # view yaml files for static pods
ls /etc/kubernetes/pki # view certificates for all components


# in case of k8s cluster build from scratch
# check following service or logs on master nodes
systemctl status kube-apiserver  
sytemctl status kube-controller-manager
systemctl status kube-scheduler
sudo journalctl -u kube-apiserver

# check following service on worker nodes
systemctl status kubelet -l
systemctl status kube-proxy

```
## 3. worker nodes failure
```bash
kubectl get nodes
kubectl describe node worker01
top # check cpu, memory usage
df -h  # check disc usage
sytemctl status kubelet.service # check kubelet status
sytemctl status kubelet.service -l # look for addtional logs
systemctl restart kubelet # try restart kubelet
sytemctl status kubelet.service -l # look for addtional logs again

sudo journalctl -u kubelet # check kubelet logs
cd /etc/systemd/system/kubelet.service.d/ # check kubelet config file location
cat /var/lib/kubelete/config.yaml # check kubelet config yaml file

systemctl daemon-reload
systemctl restart kubelet


openssl x509 -in /var/lib/kubelet/worker01.crt -text # check kubelet certificate







```
