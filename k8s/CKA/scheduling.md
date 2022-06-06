# Scheduling
## 1. taints, tolerations and affinity

```yaml
spec:
  containers:
  nodeSelector:
    size: Large
```
```bash
kubectl label nodes node01 size=Large
https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
```
## 2. requests and limits

https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/

https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/

## 3. daemonset and static pods

https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/

https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/

## 4. multiple scheduler
https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/

https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/

## 5. monitoring logging debugging
```bash
git clone https://github.com/kodekloudhub/kubernetes-metrics-server.git
cd kubernetes-metrics-server
kubectl create -f .
kc top node
kc top pod
kc logs pod-name [container-name]

https://kubernetes.io/docs/tasks/debug-application-cluster/
```
