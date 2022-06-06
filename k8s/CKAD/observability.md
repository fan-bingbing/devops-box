# Observability
## 1.readiness/liveness probe
### using httpGet
```yaml
spec:
  containers:
    - name:
      readinessProbe:
        httpGet:
          path: /api/ready
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 8
```
### using tcpSocket
```yaml
spec:
  containers:
    - name:
      readinessProbe:
        tcpSocket:
          port: 3306
```
### using script
```yaml
spec:
  containers:
    - name:
      readinessProbe:
        exec:
          command:
            - cat
            - /app/is-ready
```
## 2.container logging
```bash
kubectl logs -f pod-name
kubectl logs -f pod-name container-name # multi-container pod
```
## 3.in-memory monitoring
```bash
minikube addons enable metrics-server

git clone https://github.com/kubernetes-incubator/merics-server.git
kubectl create -f deploy/1.8+/
kubectl top node
kubectl top pod
```
