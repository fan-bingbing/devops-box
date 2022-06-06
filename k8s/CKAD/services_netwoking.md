# Services and Networking
## 1.Sevices
### sevice definition
```yaml
spec:
  type: NodePort
  ports:
  - targePort: 80
    port: 80
    nodePort: 30008
  selector:
    app: myapp
    type: frontend
```
```bash
kubectl create -f svc-definition.yaml
kubectl get services
curl http://192.168.1.1:30008
```
## 2.Ingress
### ingress-controller-deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress
spec:
```
### ingress-controller-configmap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-ingress
```
### ingress-controller-service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress
spec:
  type: NodePort
  ports:
  - port: 80
  - port: 443
  selector:
    name: nginx-ingress
```
### ingress-controller-serviceaccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress
```
### ingress-resource
#### spliting traffic by one rule/multi paths
```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /wear
        backend:
          serviceName: wear-service
          servicePort: 80
      - path: /watch
        backend:
          serviceName: watch-service
          servicePort: 80
```
#### spliting traffic by multi rules/multi paths
```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
  - host: wear.domain
    http:
      paths:
      - backend:
          seviceName: wear-service
          servicePort: 80
  - host: watch.domain
    http:
      paths:
      - backend:
          seviceName: watch-service
          servicePort: 80
```
```bash
kubectl create -f ingress-wear.yaml
kubectl get ingress
kubectl describe ingress ingress-wear
```
## 3.Network policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
    ports:
    - protocol: TCP
      port: 3306
```
```bash
kubectl create -f policy-definition.yaml

```
