# Multi-container pod
## definition in yaml file
```yaml
spec:
  containers:
    - name: webapp
      image: nginx
    - name: log-agent
      image: log-agent
  initContainers:
    - name: init-myservice
      image: busybox:1.28
      command: ['sh', '-c', "..."]

```
