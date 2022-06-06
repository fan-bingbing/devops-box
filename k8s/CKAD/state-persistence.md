# State persistence
## 1.PV
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessModes:
  - ReadWriteOnce
  capacity:
    storage: 10Gi
  hostPath:
    path: /tmp/data
  awsElasticBlockStore:
    volumeID:
    fsType: ext4
```
```bash
kubectl create -f pv-definition.yaml
kubectl get persistenctvolume
```
## 2.PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```
```bash
kubectl create -f pvc-definition.yaml
kubectl get persistenctvolumeclaim
kubectl delete persistenctvolumeclaim
```
## 3.Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: myfrontend
    image: nginx
    volumeMounts:
    - mountPath: "/var/www/html"
      name: mypd
  volumes:
  - name: mypd
    persistentVolumeClaim:
      claimName: myclaim
```
