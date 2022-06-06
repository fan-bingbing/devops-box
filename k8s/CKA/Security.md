# Security
## 1. security primitives: TLS knowledge

### symmetric encryption: use same key to encrypt/decrypt data, exchange key between sender and receiver
```bash
# man in the middle can sniff traffic, get symmetric key and hack users account
```
### asymmetric encryption: private/public key pair encryption such as SSH to remote server
#### a. on client side:
```bash
ssh-keygen
# generate private and public keys: id_rsa, id_rsa.pub
```
#### b. on server side:
```bash
cat ~/.ssh/authorized.keys
# copy over public key from client side, check it
# copy over public keys to as many servers as you want
```
#### c. log into server from client
```bash
ssh -i id_rsa user1@server1
```
### asymmetric encryption: private/public key pair encryption such as SSL
#### a. on server side:
```bash
openssl genrsa -out my-bank.key 1024
# generate private key my-bank.key
openssl rsa -in my-bank.key -pubout > mybank.pem
# generate public key mybank.pem
```
#### b. on client side:
```bash
https://my-bank.com
# public key gets transferred to client from server
# use public key provided by server to encrypt symmetric key , send encrypted symmetric key to server
# server use private key to decrypt the content, get symmetric key
# now symmetric key are safely available only for client and server
# now client can use symmetric key to encrypt data (username, password), send it to server, server can also decrypt it.
# by this way, man in the middle don't have private key, so they can't do anything.
```
#### c1. problems: hacker make a fake server with SSL keys setup, client data(username, password) can be hacked!
#### c2. solutions: digital certificates that certifies public key from server to verify server's identity
#### c3. who signed and issued certificate: only CA signed certificates are safe
#### c4.1. browser check certificates https://my-bank.com
#### c4.2. CA: certificate authorities: Symantec, digicert, GlobalSign ...
```bash
openssl req -new -key my-bank.key -out my-bank.csr -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my-bank.com"
# generate certificate signing request: my-bank.key my-bank.csr
# generate certificate signing request, CA validate information, sign and send certificate back
```
#### c4.3. CA issue their own private and public keys, public keys are stored in browsers, so browsers can validate CA are themselves, check trusted CA in browser settings
#### c4.4. private CA options within organizations provided by CA
#### c4.5. client certificates are not implemented or implemented under the hook on web servers.
#### c5. this forms PKI(Public Key Infrastructure), clients in the end can use username and password safely through https://my-bank.com



## 2. TLS in kubernetes
### Naming conventions:
```bash
# *.crt *.pem are public keys(with certificates)
# *.key, *-key.pem are private keys
```
### Certificates in kubernetes: Root certificates from CA, Server certificates, Client certificates
#### a. create root certificate
```bash
openssl genrsa -out ca.key 2048
# create private key
openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.csr
# create signing request
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
# sign certificate using its own private key
```
#### b. create admin client certificate
```bash
openssl genrsa -out admin.key 2048
# create private key for admin
openssl req -new -key admin.key -subj "/CN=kube-admin/O=system:masters" -out admin.csr
# create signing request for admin with admin privileges
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
# sign certificate using CA key pair, get admin.crt
# ca.crt need to be specified for all other certificates
```
#### c. same procedures to create other client certificates
#### d. create server certificates
#### e. view certificates in kubeadm cluster
```bash
cat /etc/kubernetes/manifests/kube-apiserver.yaml
# get certificates file names
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
# view these files one by one
# health check: Subject, Subject Alternative Names, Issuer, Validity
kubectl logs etcd-master
docker ps -a
docker logs container-id
```
#### f. manage certificates, certificates API
```bash
openssl genrsa-out jane.key 2048
# user jane generate a private key
openssl -req -new -key jane.key -subj "/CN=jane/O=jane" -out jane.csr
# user jane create a signing request
cat jane.csr | base64
# admin encode jane.csr and create a CSR object file: jane-csr.yaml
kubectl get csr
kubectl certificate approve jane

kubectl certificate deny jane # deny csr
kubectl delete csr jane # delete csr

kubectl get csr jane -o yaml
echo "LS0...Qo" | base64 -d
# admin approve csr, decode it, share certificate with jane
cat /etc/kubernetes/manifests/kube-controller-manager.yaml
# controller-manage did the job under hook
```
#### g. kubeconfig
```yaml
apiVersion: v1
kind: Config
clusters:
contexts:
users:
```
```bash
cat ~/.kube/config # file that defines clusters/context/users
kubectl config view # use default config file
kubectl config view --kubeconfig=my-custom-config # user customized config file
kubectl config --current --namespace=... # change namespace

kubectl config use-context prod-user@production # change current context
kubectl config -h # explore more options

```

#### h. API groups
```bash
curl http://localhost:6443 -k # denied

kubectl proxy --port=8001
# starting to serve on 127.0.0.1:8001, relay credentials from kubeconfig file
curl http://localhost:8001 | less
curl http://localhost:8001/version
# gain authentication to kube-api-server

# tmux keys: ctrl+b ; --> split pane horizontally
# tmux keys: ctrl+b % --> split pane vertically
# tmux keys: ctrl+b up/down/left/right --> toggle panes
```

#### i. RBAC (Role Based Access Control, authorize resources in a namespace)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
rules:
```
```bash
kubectl create -f developer-role.yaml
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
subjects:
roleRef:
```
```bash
kubectl create -f developer-role-rolebinding.yaml
kubectl get roles
kubectl get rolebindings
kubectl describe role developer
kubectl describe rolebinding devuser-developer-binding

#as user dev-user to check what dev-user can or can not  do
kubectl auth can-i create deployments
kubectl auth can-i delete nodes

#as admin to check what dev-user can or can not do
kubectl auth can-i create deployments --as dev-user
kubectl auth can-i create pods --as dev-user
kubectl auth can-i create pods --as dev-user --namespace test

https://kubernetes.io/docs/reference/access-authn-authz/rbac/
```
#### j. Cluster Roles and RoleBindings to authorize cluster wide resources
```bash
kubectl api-resources --namespaced=true # e.g.: pods, deployments
kubectl api-resources --namespaced=false # e.g.: nodes, PVs
# list namespaced resources or cluster scoped resources
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
rules:
# ClusterRole can assign namespaced resources as well, across cluster
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
subjects:
roleRef:
```
```bash
kubectl create -f file.yaml
https://kubernetes.io/docs/reference/access-authn-authz/rbac/
```
#### k. image security for private image repository
```bash
docker login private-registry.io
docker run private-registry.io/apps/internal-app
# login private image repository in docker

kubectl create secret docker-registry regcred \
--docker-server=private-registry.io \
--docker-username=registry-user \
--docker-password=registry-password \
--docker-email=registry-user@org.com
# use private registry secret in pod definition file
https://kubernetes.io/docs/concepts/containers/images/
```
```yaml
spec:
  containers:
  - name:
    image:
  imagePullSecrets:
  - name: regcred
```
#### l. security context
```bash
https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
```
#### m. network policies
```bash
https://kubernetes.io/docs/concepts/services-networking/network-policies/
```








```
