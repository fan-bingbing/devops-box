# Configuration
## 1. commands and arguments

```Dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--color", "red"]
```
```yaml
#k8s yaml overwrite ENTRYPOINT
command: ["python", "app.py"]
#k8s yaml overwrite CMD
args: ["--color", "red"]
```
## 2. configmaps
### create from literal
```bash
kubectl create configmap \
app-config --from-literal=APP_COLOR=blue
```
### create from file
```bash
kubectl create configmap \
app-config --from-file=app_config.properties
```

### revise pod definition file
```yaml
spec:
  containers:
    - envFrom:
        - configMapRef:
            name: app-config

```

### view
```bash
kubectl get configmaps
kubectl get secrets
kubectl get secret app-secret -o yaml
kubectl describe secret app-secret
kubectl describe configmap app-config
```
## 3. secret
### create from literal
```bash
kubectl create secret generic \
app-secret --from-literal=DB_Password=passwd
```
### create from file
```bash
kubectl create secret generic \
app-secret --from-file=app-secret.properties
```
### convert between plaintext and base64
```bash
echo -n "passwd" | base64 # encoding is not encryption
echo -n "bXlzcWW=" | base64 --decode # decoding
```
### revise pod definition file
```yaml
spec:
  containers:
    - envFrom:
        - secretRef:
            name: app-secret


```
## 4. security context
### revise pod definition file
```yaml
spec:
  containers:
    - securityContext:
        runAsUser: 0 # root
        capabilities:
          add: ["MAC_ADMIN"]

```
## 5. service account (for api authenciation)
### create service account
```bash
kubectl create serviceaccount dashboard-sa
kubectl get serviceaccount
kubectl describe serviceaccount dashboard-sa
kubectl describe secret dashboard-sa-token-kbbdm
# use this token for k8s-api authentication
```
### revise pod definition part in deloyment yaml
```yaml
spec:
  containers:
  serviceAccount: dashboard-sa
```
### to disable auto-mount default service account
```yaml
spec:
  containers:
  automountServiceAccountToken: false
```
### default service account
```bash
kubectl exec -it dashboard ls /var/run/secrets/kubernetes.io/serviceaccount
kubectl exec -it dashboard cat /var/run/secrets/kubernetes.io/serviceaccount/token
```
## 6. resource request
```yaml
spec:
  containers:
    - resources:
        requests:
          memory: "1Gi"
          cpu: 1
        limits:
          memory: "2Gi"
          cpu: 2
```
## 7. taints-node
### create taint on node1
```bash
kubectl taint nodes node1 app=blue:NoSchedule
# NoExecute means pod that is not tolerant will be evicted.
kubectl describe node kubemaster | grep Taint
# master node is configured not to schedule any app pods
kubectl get nodes
# get all nodes
kubectl taint nodes $(hostname) node-role.kubernetes.io/master:NoSchedule-
# untaint master node
```
### revise pod definition
```yaml
spec:
  containers:
  tolerations:
    - key: "app"
      operator: "Equal"
      value: "blue"
      effect: "NoSchedule"
```
## 7. node selectors, node affinity
### label a node
```bash
kubectl label nodes node1 size=Large
```
### revise pod definition in simple way
```yaml
spec:
  containers:
  nodeSelector:
    size: Large
```
### revise pod definition in complex way
```yaml
spec:
  containers:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: In
                values:
                  - Large
                  - Medium
```
