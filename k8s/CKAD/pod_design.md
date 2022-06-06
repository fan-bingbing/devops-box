# Pod design
## 1.labels and annotations
### labels in pod definition
```yaml
metadata:
  labels:
    app: app1
    function: front-end
```
### select pod with labels
```bash
kubectl get pods -l app=app1,function=front-end
```
### labels in replicaset definition
```yaml
metadata:
  labels:
    app: app1
    function: front-end
  annotations:
    buildversion: 1.34
spec:
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
        function: front-end
```
## 2.rollout and rollback
### strategies: recreate or rolling update

```bash
kubectl run nginx --image=nginx
kubectl create -f dp-definistion.yaml --record
kubectl apply -f dp-definistion.yaml
kubectl rollout undo deployment/myapp-deployment
kubectl rollout status deployment/myapp-deployment
kubectl rollout history deployment/myapp-deployment --revision=1
```
## 2.jobs and cronjobs
### a simple addition job in docker
```bash
docker run ubuntu expr 3 + 4
docker ps -a
```
### a simple addition job in a pod in k8s
```yaml
spec:
  containers:
    - name: math-add
      image: ubuntu
      command: ['expr', '3', '+', '4']
  restartPolicy: Always # or Never
```
```bash
kubectl create -f pod-definition.yaml
kubectl get pods
```
### a job yaml file
```yaml
apiVersion: batch/v1 # may change over time
kind: Job
metadata:
  name: math-add-job
spec:
  completions: 3 # create 3 pods
  parallelism: 3 # create 3 pods in parallel
  backoffLimit: 4
  template:
    spec:
      containers:
        - name: math-add
          image: ubuntu
          command: ['expr', '3', '+', '4']
      restartPolicy: Never
```
```bash
kubectl create -f job-definition.yaml
kubectl get jobs
kubectl get pods # completed status with 0 restart
kubectl logs math-add-job-xxx # check output 7
kubectl describe math-add-job-xxx
kubectl delete job math-add-job-xxx # result in delete container
```
### a cronjob yaml file
```yaml
apiVersion: batch/v1beta1 # may change over time
kind: Cronjob
metadata:
  name: reporting-cronjob
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      completions: 3 # create 3 pods
      parallelism: 3 # create 3 pods in parallel
      template:
        spec:
          containers:
            - name: math-add
              image: ubuntu
              command: ['expr', '3', '+', '4']
          restartPolicy: Never
```
