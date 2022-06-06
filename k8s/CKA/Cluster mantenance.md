# Cluster mantenance
## 1. OS upgrades
```bash
# k8s wait for node back on line before considering it's dead
kube-controller-manager --pod-eviction-timeout=5m0s ...
# node comes up blank after 5min without any pod scheduled
# pods created without replicaset are just gone

kubectl drain node-1 # terminate node-1, move pods to other existing nodes, node-1 becomes unschedulable
kubectl uncordon node-1 # node-1 becomes schedulable
kubectl cordon node-2 # node-2 becomes unschedulable but still alive
kubectl get events # check which app deployed on which node

```
## 2. K8S software version and cluster upgrade process
### master node version upgrade
```bash
kubeadm upgrade plan # upgrade information
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/
```
### worker node version upgrade
```bash
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

```
## 3. backup and restore
### candidate1: resource configuration > yaml files to github
```bash
kubectl get all --all-namespaces -o yaml > all-deploy-services.yaml
```
### candidate2: ETCD server
```bash
https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/recovery.md#restoring-a-cluster
ETCDCTL_API=3 etcdctl snapshot save snapshot.db
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db
# init
```
### candidate3: PV(persistent volume)
