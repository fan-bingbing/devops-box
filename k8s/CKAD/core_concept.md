# Core concept
## 1. Pods
```bash
kubectl run nginx --image=nginx --restart=Never --dry-run -o
kubectl get pods
kubectl describe pod nginx
kubectl get pod nginx -o yaml > pod-nginx.yaml
kubectl delete pod nginx
kubectl create -f pod-nginx.yaml
kubectl edit pod nginx
```
## 2. ReplicaSet
```bash
kubectl get replicaset
kubectl create -f rc-definition.yaml
kubectl replace -f rc-definition.yaml
kubectl scale --replicas=6 replicaset myapp-rc
```
## 3. Deployment
```bash
kubectl get deployments
kubectl create -f dp-definition.yaml
kubectl create deployment mydp --image=nginx
kubectl create deployment mydp --image=nginx --dry-run -o yaml
kubectl scale deployment mydp --replicas=5

```
## 3. Namespace
```bash
kubectl get namespaces
kubectl create namespace dev
kubectl create -f ns-definition.yaml
kubectl get pods -n dev
kubectl config set-context $(kubectl config current-context) --namespace=dev
kubectl get pods --all-namespaces
kubectl create quota myqt --hard=cpu=1,memory=1G,pods=2
kubectl create quota myqt --hard=cpu=1,memory=1G,pods=2 --dry-run -o yaml
```
## 3. Service
```bash
kubectl
```
## how to copy/paste in nano
```bash
setmark: CTL+6
select: use arrow to higtlight text
copy: ALT+6
paste: CTL+u
delete: CTL+k
show line numbers: CTL+C
```
