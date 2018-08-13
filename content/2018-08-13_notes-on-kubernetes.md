Title: Notes on Kubernetes
Date: 2018-08-13- 14:54
Modified: 2018-08-13- 14:54
Category: posts
Tags: DevOps, Kubernetes, Docker, Traefik, LoadBalancer, helm, weave, 
Slug: noted-on-kubernetes
Authors: Jitse-Jan
Summary: After numerous restarts and resets of my VPS and executing over 20 different tutorials, I finally have my receipe to get my single node Kubernetes cluster with a proper load balancer working. Please note that the last version of my Kubernetes experiment can be found on my [Git repo](https://github.com/jitsejan/kubernetes-dev). Remember that this repository mainly contains a variety of YAML files that got the system working. What worked for me, might not work for anyone else. 

## TLDR:
Final solution:

* `docker`
* `kubeadm`
* `kubectl`
* `kubelet`
* `helm`
* `weave`
* `heapster`
* `traefik` 

## Sources
Some of the sources I have used to get my Kubernetes cluster up and running:

* [Kubernetes in 10 minutes](https://blog.alexellis.io/kubernetes-in-10-minutes/)
* [Your instant Kubernetes cluster](https://blog.alexellis.io/your-instant-kubernetes-cluster/)
* [Setting up a single node Kubernetes Cluster](https://ninetaillabs.com/setting-up-a-single-node-kubernetes-cluster/)
* [Kubernetes On Bare Metal](https://joshrendek.com/2018/04/kubernetes-on-bare-metal/)
* [Kubernetes : Ingress Controller with Træfɪk and Let's Encrypt](https://blog.osones.com/en/kubernetes-ingress-controller-with-traefik-and-lets-encrypt.html)


## Walkthrough
Before we begin, update the system:
```
jitsejan@dev16:~$ sudo apt-get update
```

### Install Docker
<center><img src="http://files.jitsejan.com/logos/docker.PNG" width=200/></center>

```bash
jitsejan@dev16:~$ sudo apt-get install -qy docker.io
jitsejan@dev16:~$ docker --version
Docker version 17.03.2-ce, build f5ec1e2
```
### Install Kubernetes apt repository

<center><img src="http://files.jitsejan.com/logos/kubernetes.svg" width=200/></center>

```bash
jitsejan@dev16:~$ sudo apt-get install -y apt-transport-https && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
jitsejan@dev16:~$ echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" \
  | sudo tee -a /etc/apt/sources.list.d/kubernetes.list \
  && sudo apt-get update 
```

### Install `kubeadm`, `kubectl` and `kubelet`
```bash
jitsejan@dev16:~$ sudo apt-get install -y kubelet kubeadm kubectl
jitsejan@dev16:~$ kubelet --version
Kubernetes v1.11.1
jitsejan@dev16:~$ kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"11", GitVersion:"v1.11.1", GitCommit:"b1b29978270dc22fecc592ac55d903350454310a", GitTreeState:"clean", BuildDate:"2018-07-17T18:50:16Z", GoVersion:"go1.10.3", Compiler:"gc", Platform:"linux/amd64"}
jitsejan@dev16:~$ kubectl version
Client Version: version.Info{Major:"1", Minor:"10", GitVersion:"v1.10.0", GitCommit:"fc32d2f3698e36b93322a3465f63a14e9f0eaead", GitTreeState:"clean", BuildDate:"2018-03-26T16:55:54Z", GoVersion:"go1.9.3", Compiler:"gc", Platform:"linux/amd64"}
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

### Initialize kubernetes
```bash
jitsejan@dev16:~$ sudo kubeadm init
[init] using Kubernetes version: v1.11.1
[preflight] running pre-flight checks
I0807 05:46:52.371257    3480 kernel_validator.go:81] Validating kernel version
I0807 05:46:52.371519    3480 kernel_validator.go:96] Validating kernel config
[preflight/images] Pulling images required for setting up a Kubernetes cluster
[preflight/images] This might take a minute or two, depending on the speed of your internet connection
[preflight/images] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[preflight] Activating the kubelet service
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [dev16.jitsejan.com kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 142.44.184.35]
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated sa key and public key.
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Generated etcd/ca certificate and key.
[certificates] Generated etcd/server certificate and key.
[certificates] etcd/server serving cert is signed for DNS names [dev16.jitsejan.com localhost] and IPs [127.0.0.1 ::1]
[certificates] Generated etcd/peer certificate and key.
[certificates] etcd/peer serving cert is signed for DNS names [dev16.jitsejan.com localhost] and IPs [142.44.184.35 127.0.0.1 ::1]
[certificates] Generated etcd/healthcheck-client certificate and key.
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/scheduler.conf"
[controlplane] wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests" 
[init] this might take a minute or longer if the control plane images have to be pulled
[apiclient] All control plane components are healthy after 46.003711 seconds
[uploadconfig] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.11" in namespace kube-system with the configuration for the kubelets in the cluster
[markmaster] Marking the node dev16.jitsejan.com as master by adding the label "node-role.kubernetes.io/master=''"
[markmaster] Marking the node dev16.jitsejan.com as master by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "dev16.jitsejan.com" as an annotation
[bootstraptoken] using token: j8gf09.pe16y63l0hxygc77
[bootstraptoken] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 142.44.184.35:6443 --token j8gf09.pe16y63l0hxygc77 --discovery-token-ca-cert-hash sha256:d8d47cbd352035d5a7746d0ed7e54ae7c0c6bcbb5e89ef410039f7b457be853f

```
Run the steps mentioned in the previous output:
```
jitsejan@dev16:~$ mkdir -p $HOME/.kube
jitsejan@dev16:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
jitsejan@dev16:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### Weave net
```
jitsejan@dev16:~$ export kubever=$(kubectl version | base64 | tr -d '\n')
jitsejan@dev16:~$ kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$kubever"
serviceaccount/weave-net created
clusterrole.rbac.authorization.k8s.io/weave-net created
clusterrolebinding.rbac.authorization.k8s.io/weave-net created
role.rbac.authorization.k8s.io/weave-net created
rolebinding.rbac.authorization.k8s.io/weave-net created
daemonset.extensions/weave-net created
```

### Untaint the master node
Make sure we can install pods on the master node:
```
jitsejan@dev16:~$ kubectl taint nodes --all node-role.kubernetes.io/master-
node/dev16.jitsejan.com untainted
```

Check status of the pods:
```bash
jitsejan@dev16:~$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                         READY     STATUS    RESTARTS   AGE
kube-system   coredns-78fcdf6894-2khbk                     1/1       Running   0          4m
kube-system   coredns-78fcdf6894-flmnd                     1/1       Running   0          4m
kube-system   etcd-dev16.jitsejan.com                      1/1       Running   0          3m
kube-system   kube-apiserver-dev16.jitsejan.com            1/1       Running   0          3m
kube-system   kube-controller-manager-dev16.jitsejan.com   1/1       Running   0          4m
kube-system   kube-proxy-59l87                             1/1       Running   0          4m
kube-system   kube-scheduler-dev16.jitsejan.com            1/1       Running   0          4m
kube-system   weave-net-rkmrb                              2/2       Running   0          1m
```

## Install `helm`
Install the package manager for Kubernetes:
```bash
jitsejan@dev16:~$ sudo snap install helm
2018-08-07T06:04:43-07:00 INFO Waiting for restart...
helm 2.9.1 from 'snapcrafters' installed
jitsejan@dev16:~$ sudo kubectl create -f ./helm-rbac.yml
serviceaccount/tiller created
clusterrolebinding.rbac.authorization.k8s.io/tiller created
jitsejan@dev16:~$ sudo cp ~/.kube/config /root/snap/helm/common/kube/config
jitsejan@dev16:~$ sudo helm init --service-account tiller
Creating /root/snap/helm/common/repository 
Creating /root/snap/helm/common/repository/cache 
Creating /root/snap/helm/common/repository/local 
Creating /root/snap/helm/common/plugins 
Creating /root/snap/helm/common/starters 
Creating /root/snap/helm/common/cache/archive 
Creating /root/snap/helm/common/repository/repositories.yaml 
Adding stable repo with URL: https://kubernetes-charts.storage.googleapis.com 
Adding local repo with URL: http://127.0.0.1:8879/charts 
$HELM_HOME has been configured at /root/snap/helm/common.

Tiller (the Helm server-side component) has been installed into your Kubernetes Cluster.

Please note: by default, Tiller is deployed with an insecure 'allow unauthenticated users' policy.
For more information on securing your installation see: https://docs.helm.sh/using_helm/#securing-your-helm-installation
Happy Helming!
jitsejan@dev16:~/kubernetes-dev$ sudo helm version --short
Client: v2.9.1+g20adb27
Server: v2.9.1+g20adb27
```

Check status of the pods:
```
jitsejan@dev16:~/kubernetes-dev$ kubectl get pods --all-namespaces
NAMESPACE        NAME                                         READY     STATUS    RESTARTS   AGE
kube-system      coredns-78fcdf6894-2khbk                     1/1       Running   0          45m
kube-system      coredns-78fcdf6894-flmnd                     1/1       Running   0          45m
kube-system      etcd-dev16.jitsejan.com                      1/1       Running   0          44m
kube-system      kube-apiserver-dev16.jitsejan.com            1/1       Running   0          44m
kube-system      kube-controller-manager-dev16.jitsejan.com   1/1       Running   0          44m
kube-system      kube-proxy-59l87                             1/1       Running   0          45m
kube-system      kube-scheduler-dev16.jitsejan.com            1/1       Running   0          44m
kube-system      tiller-deploy-759cb9df9-ddv2h                1/1       Running   0          1m
kube-system      weave-net-rkmrb                              2/2       Running   0          41m
```


## Heapster

```
jitsejan@dev16:~/kubernetes-dev$ sudo helm install stable/heapster --name heapster --set rbac.create=true
NAME:   heapster
LAST DEPLOYED: Tue Aug  7 10:04:28 2018
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Service
NAME      TYPE       CLUSTER-IP    EXTERNAL-IP  PORT(S)   AGE
heapster  ClusterIP  10.108.195.4  <none>       8082/TCP  1s

==> v1beta1/Deployment
NAME               DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
heapster-heapster  1        1        1           0          1s

==> v1/Pod(related)
NAME                                READY  STATUS             RESTARTS  AGE
heapster-heapster-7bb6d67b9d-h77tj  0/2    ContainerCreating  0         0s

==> v1/ServiceAccount
NAME               SECRETS  AGE
heapster-heapster  1        1s

==> v1beta1/ClusterRoleBinding
NAME               AGE
heapster-heapster  1s

==> v1beta1/Role
NAME                         AGE
heapster-heapster-pod-nanny  1s

==> v1beta1/RoleBinding
NAME                         AGE
heapster-heapster-pod-nanny  1s


NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app=heapster-heapster" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace default port-forward $POD_NAME 8082
```




## Traefik

<center><img src="http://files.jitsejan.com/logos/traefik.PNG" width=200/></center>


> Træfik is a modern HTTP reverse proxy and load balancer that makes deploying microservices easy. Træfik integrates with your existing infrastructure components (Docker, Swarm mode, Kubernetes, Marathon, Consul, Etcd, Rancher, Amazon ECS, ...) and configures itself automatically and dynamically. Pointing Træfik at your orchestrator should be the only configuration step you need.

[Docs](https://docs.traefik.io/user-guide/kubernetes/)


```yaml
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
rules:
  - apiGroups:
      - ""
    resources:
      - services
      - endpoints
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik-ingress-controller
subjects:
- kind: ServiceAccount
  name: traefik-ingress-controller
  namespace: kube-system
```

```bash
jitsejan@dev16:~/kubernetes-dev$ kubectl apply -f traefik-rbac.yml 
clusterrole.rbac.authorization.k8s.io/traefik-ingress-controller created
clusterrolebinding.rbac.authorization.k8s.io/traefik-ingress-controller created
jitsejan@dev16:~/kubernetes-dev$ kubectl apply -f traefik-deployment.yml 
serviceaccount/traefik-ingress-controller created
deployment.extensions/traefik-ingress-controller created
service/traefik-ingress-service created
jitsejan@dev16:~/kubernetes-dev$ kubectl --namespace=kube-system get pods
NAME                                          READY     STATUS    RESTARTS   AGE
coredns-78fcdf6894-2khbk                      1/1       Running   0          1h
coredns-78fcdf6894-flmnd                      1/1       Running   0          1h
etcd-dev16.jitsejan.com                       1/1       Running   0          1h
kube-apiserver-dev16.jitsejan.com             1/1       Running   0          1h
kube-controller-manager-dev16.jitsejan.com    1/1       Running   0          1h
kube-proxy-59l87                              1/1       Running   0          1h
kube-scheduler-dev16.jitsejan.com             1/1       Running   0          1h
tiller-deploy-759cb9df9-ddv2h                 1/1       Running   0          17m
traefik-ingress-controller-6f6d87769d-5nrvq   1/1       Running   0          20s
weave-net-rkmrb                               2/2       Running   0          58m
jitsejan@dev16:~/kubernetes-dev$ kubectl get services --namespace=kube-system
NAME                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                       AGE
kube-dns                  ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP                 1h
tiller-deploy             ClusterIP   10.106.232.150   <none>        44134/TCP                     18m
traefik-ingress-service   NodePort    10.106.201.31    <none>        80:30321/TCP,8080:32262/TCP   1m
jitsejan@dev16:~/kubernetes-dev$ curl -X GET 10.106.201.31
404 page not found
```

Check the pods:

```bash
jitsejan@dev16:~/kubernetes-dev$ kubectl get pods --all-namespaces
NAMESPACE        NAME                                          READY     STATUS    RESTARTS   AGE
kube-system      coredns-78fcdf6894-2khbk                      1/1       Running   0          1h
kube-system      coredns-78fcdf6894-flmnd                      1/1       Running   0          1h
kube-system      etcd-dev16.jitsejan.com                       1/1       Running   0          1h
kube-system      kube-apiserver-dev16.jitsejan.com             1/1       Running   0          1h
kube-system      kube-controller-manager-dev16.jitsejan.com    1/1       Running   0          1h
kube-system      kube-proxy-59l87                              1/1       Running   0          1h
kube-system      kube-scheduler-dev16.jitsejan.com             1/1       Running   0          1h
kube-system      tiller-deploy-759cb9df9-tgnkq                 1/1       Running   0          5m
kube-system      traefik-ingress-controller-66f46799fd-54pkj   1/1       Running   0          2m
kube-system      traefik-ingress-controller-66f46799fd-f42wk   1/1       Running   0          2m
kube-system      traefik-ingress-controller-external-0         1/1       Running   0          30s
kube-system      traefik-ingress-controller-external-1         1/1       Running   0          28s
kube-system      weave-net-rkmrb                               2/2       Running   0          1h
metallb-system   controller-67cb74b4b5-4ll62                   1/1       Running   0          1h
metallb-system   speaker-bbqnd                                 1/1       Running   0          1h
```

---

## Alternatives
---

### Minikube

<center><img src="http://files.jitsejan.com/logos/minikube.PNG" width=100/></center>

> Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.

Use [Minikube](https://github.com/kubernetes/minikube) to install a single node Kubernetes cluster. I didn't go for this solution, because it requires too much additional configuration to get it properly running on a VPS. I have tried with different virtualization techniques, but KVM, KVM2 and VirtualBox all had their issues. I ended up using `vm-driver=none`, which means you run Kubernetes directly on Linux, but requires you to be root.. Locally this is the preferred way of testing Kubernetes if you are not using Docker for Desktop, which has [native support](https://blog.docker.com/2018/04/docker-desktop-certified-kubernetes/) for Kubernetes. Minikube is under heavy development and the community strives to make this the **default** way of testing Kubernetes for developers.

#### Install
```bash
jitsejan@dev16:~$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube
jitsejan@dev16:~$ minikube version
minikube version: v0.28.2
```
#### Start the Kubernetes cluster
```
jitsejan@dev16:~$ sudo minikube start --vm-driver=none
Starting local Kubernetes v1.10.0 cluster...
Starting VM...
Getting VM IP address...
Moving files into cluster...
Downloading kubeadm v1.10.0
Downloading kubelet v1.10.0
Finished Downloading kubelet v1.10.0
Finished Downloading kubeadm v1.10.0
Setting up certs...
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
===================
WARNING: IT IS RECOMMENDED NOT TO RUN THE NONE DRIVER ON PERSONAL WORKSTATIONS
	The 'none' driver will run an insecure kubernetes apiserver as root that may leave the host vulnerable to CSRF attacks

When using the none driver, the kubectl config and credentials generated will be root owned and will appear in the root home directory.
You will need to move the files to the appropriate location and then set the correct permissions.  An example of this is below:

	sudo mv /root/.kube $HOME/.kube # this will write over any previous configuration
	sudo chown -R $USER $HOME/.kube
	sudo chgrp -R $USER $HOME/.kube

	sudo mv /root/.minikube $HOME/.minikube # this will write over any previous configuration
	sudo chown -R $USER $HOME/.minikube
	sudo chgrp -R $USER $HOME/.minikube

This can also be done automatically by setting the env var CHANGE_MINIKUBE_NONE_USER=true
Loading cached images from config file.
```

```
jitsejan@dev16:~$ sudo kubectl config current-context
minikube
```

### Flannel (instead of Weave)

<center><img src="http://files.jitsejan.com/logos/metallb.PNG" width=100/></center>

Another network layer for the containers that can be used is [flannel](https://coreos.com/flannel/docs/latest/).

> flannel is a virtual network that gives a subnet to each host for use with container runtimes.
> 
> Platforms like Google's Kubernetes assume that each container (pod) has a unique, routable IP inside the cluster. The advantage of this model is that it reduces the complexity of doing port mapping.

```bash
jitsejan@dev16:~$ kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address 142.44.184.35
jitsejan@dev16:~$ wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
jitsejan@dev16:~$ kubectl create -f kube-flannel.yml --namespace=kube-system
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds-amd64 created
daemonset.extensions/kube-flannel-ds-arm64 created
daemonset.extensions/kube-flannel-ds-arm created
daemonset.extensions/kube-flannel-ds-ppc64le created
daemonset.extensions/kube-flannel-ds-s390x created

jitsejan@dev16:~$ kubectl get nodes
NAME                 STATUS    ROLES     AGE       VERSION
dev16.jitsejan.com   Ready     master    7m        v1.11.1

jitsejan@dev16:~$ kubectl get pods -n kube-system
NAME                                         READY     STATUS    RESTARTS   AGE
coredns-78fcdf6894-lfrf9                     1/1       Running   0          8m
coredns-78fcdf6894-tblp9                     1/1       Running   0          8m
etcd-dev16.jitsejan.com                      1/1       Running   0          7m
kube-apiserver-dev16.jitsejan.com            1/1       Running   0          7m
kube-controller-manager-dev16.jitsejan.com   1/1       Running   0          7m
kube-flannel-ds-amd64-bgdhb                  1/1       Running   0          1m
kube-proxy-mz7jt                             1/1       Running   0          8m
kube-scheduler-dev16.jitsejan.com            1/1       Running   0          7m
```


### Calico (instead of Weave) 

<center><img src="http://files.jitsejan.com/logos/calico.JPG" width=200/></center>


Instead of using Weave or Flannel, we can use [`Calico`](https://docs.projectcalico.org/master/getting-started/kubernetes/) to create a virtual network in our Kubernetes cluster.


```bash
jitsejan@dev16:~$ sudo kubectl apply -f https://docs.projectcalico.org/master/getting-started/kubernetes/installation/hosted/etcd.yaml
daemonset.extensions "calico-etcd" created
service "calico-etcd" created
jitsejan@dev16:~$ sudo kubectl apply -f https://docs.projectcalico.org/master/getting-started/kubernetes/installation/rbac.yaml
clusterrole.rbac.authorization.k8s.io "calico-kube-controllers" created
clusterrolebinding.rbac.authorization.k8s.io "calico-kube-controllers" created
clusterrole.rbac.authorization.k8s.io "calico-node" created
clusterrolebinding.rbac.authorization.k8s.io "calico-node" created
jitsejan@dev16:~$ sudo kubectl apply -f \
https://docs.projectcalico.org/master/getting-started/kubernetes/installation/hosted/calico.yaml
configmap "calico-config" created
secret "calico-etcd-secrets" created
daemonset.extensions "calico-node" created
serviceaccount "calico-node" created
deployment.extensions "calico-kube-controllers" created
serviceaccount "calico-kube-controllers" created
jitsejan@dev16:~$ watch kubectl get pods --all-namespaces

Every 2.0s: kubectl get pods --all-namespaces                                                                                                                                                                 Fri Aug  3 04:57:04 2018

NAMESPACE     NAME                                         READY     STATUS    RESTARTS   AGE
kube-system   calico-etcd-926qj                            1/1       Running   0          5m
kube-system   calico-kube-controllers-bcb7959cd-5njws      1/1       Running   0          2m
kube-system   calico-node-p45mz                            2/2       Running   0          2m
kube-system   coredns-78fcdf6894-kxsff                     1/1       Running   0          7m
kube-system   coredns-78fcdf6894-r2brs                     1/1       Running   0          7m
kube-system   etcd-dev16.jitsejan.com                      1/1       Running   0          6m
kube-system   kube-apiserver-dev16.jitsejan.com            1/1       Running   0          7m
kube-system   kube-controller-manager-dev16.jitsejan.com   1/1       Running   0          7m
kube-system   kube-proxy-kb559                             1/1       Running   0          7m
kube-system   kube-scheduler-dev16.jitsejan.com            1/1       Running   0          7m
```

### metallb (instead of Traefik)

<center><img src="http://files.jitsejan.com/logos/flannel.PNG" width=200/></center>

Because we are not using EKS, AKS or GCP, we need to deal with the **load balancer** ourselves. Before I showed how to use Traefik as the load balancer to take care of all incoming traffic to the VPS, but [`metallb`[(https://metallb.universe.tf/)] could be a good alternative. My initial approach involved both Traefik and metallb, but this seemed to create overhead and Traefik has enough functionality to handle the ingress and egress by itself. 

#### Install the loadbalancer `metallb`
```bash
jitsejan@dev16:~$ kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.7.2/manifests/metallb.yaml
namespace/metallb-system created
serviceaccount/controller created
serviceaccount/speaker created
clusterrole.rbac.authorization.k8s.io/metallb-system:controller created
clusterrole.rbac.authorization.k8s.io/metallb-system:speaker created
role.rbac.authorization.k8s.io/config-watcher created
clusterrolebinding.rbac.authorization.k8s.io/metallb-system:controller created
clusterrolebinding.rbac.authorization.k8s.io/metallb-system:speaker created
rolebinding.rbac.authorization.k8s.io/config-watcher created
daemonset.apps/speaker created
deployment.apps/controller created
jitsejan@dev16:~$ kubectl get pods -n metallb-system
NAME                          READY     STATUS    RESTARTS   AGE
controller-67cb74b4b5-4ll62   1/1       Running   0          31s
speaker-bbqnd                 1/1       Running   0          31s
```

#### Configure the loadbalancer

`metallb-conf.yml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.1.16/28
```

```bash
jitsejan@dev16:~$ kubectl apply -f metallb-conf.yml 
configmap/config created
jitsejan@dev16:~$ kubectl get pods --all-namespaces
NAMESPACE        NAME                                         READY     STATUS    RESTARTS   AGE
kube-system      coredns-78fcdf6894-2khbk                     1/1       Running   0          52m
kube-system      coredns-78fcdf6894-flmnd                     1/1       Running   0          52m
kube-system      etcd-dev16.jitsejan.com                      1/1       Running   0          51m
kube-system      kube-apiserver-dev16.jitsejan.com            1/1       Running   0          51m
kube-system      kube-controller-manager-dev16.jitsejan.com   1/1       Running   0          51m
kube-system      kube-proxy-59l87                             1/1       Running   0          52m
kube-system      kube-scheduler-dev16.jitsejan.com            1/1       Running   0          51m
kube-system      tiller-deploy-759cb9df9-ddv2h                1/1       Running   0          8m
kube-system      weave-net-rkmrb                              2/2       Running   0          48m
metallb-system   controller-67cb74b4b5-4ll62                  1/1       Running   0          46m
metallb-system   speaker-bbqnd                                1/1       Running   0          46m
```