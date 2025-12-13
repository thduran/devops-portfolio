[English below]

Comandos:

```bash
# cria cluster simples (1 control-plane, 1 agente)
k3d cluster create my-cluster

# cria cluster sem LB padrão
k3d cluster create mY-cluster --no-lb

# lista clusters existentes
k3d cluster list

# deleta cluster específico 
k3d cluster delete my-cluster

# cria cluster com vários nodes (3 control-planes, 3 agentes)
k3d cluster create my-cluster --servers 3 --agents 3

# cria cluster expõe porta do host para serviços do k8s
# Ex: mapeia porta 8080 do host para porta 30000 do LB
k3d cluster create my-cluster -p "8080:30000@loadbalancer"

# comando universal para aplicar manifesto
kubectl apply -f file.yaml

# lista tudo do namespace default
kubectl get all
```

---

# Dia 01: Fundamentos e setup do ambiente

## 🚀 Por que usar Kubernetes?

Docker apenas não pode oferecer, nativamente, replicação e escalabilidade, alta dispobilidade e resiliência, load balancer, configuração unificada, rolling updates, que são essenciais em ambientes de produção.

Swarm é menos usado e não é recomendado para ambientes complexos. Além disso, Kubernetes é flexível; funciona da mesma forma on-premises ou em qualquer provedor de nuvem, evitando lock-in.

## 🏛️ Arquitetura do cluster

### 1. Control plane

Responsável por gerenciar o estado e tomar decisões globais.

*API server*: responsável pela comunicação externa e interna do cluster.
*Scheduler*: recebe requisições de criação de container do API server e decide onde executá-las.
*etcd*: banco chave-valor, armazena configurações.
*Controller manager*: gerencia controladores do k8s
*Cloud controller manager*: só aparece em ambiente cloud

### 2. Worker node

*kube-proxy*: faz comunicação de rede do cluster
*kubelet*: faz comunicação com o runtime

## Interfaces

**CRI**: (containerd, cri-o) comunicação do k8s com exterior
**CNI**: comnicação de rede do k8s (wavenet, calico, flannel)
**CSI**: comunicação com ferramentas de armazenamento

## 💡 Adicionais

* **Cluster HA:** o k8s em si precisa ter alta disponibilidade, não só os containers. Para isso, recomenda-se ter, no mínimo, 3 control planes.
* **Certifications:** CKAD é mais indicado pra devs, CKA é perfil mais infra.

## 💻 Setup COM k3d

Executa cada nó como um container Docker.

* **Minikube:** mais pesado, cria VM completa.
* **Kind:** mais replicável por ser baseado em yaml.
* **K3d:** foca na  CLI

Configuração do `kubectl` com cluster -> `~/.kube/config`. Contém credenciais, endereçamento etc.

---

English:

```bash
# simple cluster creation (1 control-plane, 1 agent)
k3d cluster create my-cluster

# creates cluster without standard LB
k3d cluster create mY-cluster --no-lb

# lists existing clusters
k3d cluster list

# deletes specific cluster
k3d cluster delete my-cluster

# creates cluster with multiple nodes (3 control-planes, 3 agents)
k3d cluster create my-cluster --servers 3 --agents 3

# creates cluster and exposes host port to k8s service
# Ex: maps port 8080 of host to port 30000 of LB
k3d cluster create my-cluster -p "8080:30000@loadbalancer"

# universal command to apply configuration manifest
kubectl apply -f file.yaml

# lists all resources of default namespace
kubectl get all
```

---

# Day 01: Fundamentals and Kubernetes setup

## 🚀 Why to use Kubernetes?

Docker only cannot serve, natively, replications and scalability, high availability and resilience, load balancing, unified configuration, rolling updates, which are critical in production-level environments.

Swarm is less used and not recommended for more complex environments. In addition, Kubernetes is flexible; it works the same way on-premises ou in any cloud provider, preventing lock-in.

## 🏛️ Kubernetes cluster architecture

### 1. Control plane

The brain, responsible for manage the state and take global decisions.

*API server*: responsible for the cluster external and internal communication.
*Scheduler*: gets container creation requisitions from API server and decides where to run them.
*etcd*: key-value database, storages configurations
*Controller manager*: manage k8s controllers
*Cloud controller manager*: only appears in cloud environments

### 2. Worker node

*kube-proxy*: responsible for cluster's network communication
*kubelet*: makes communication with the container runtime

## Kubernetes interfaces

**CRI**: (containerd, cri-o) k8s communication interface for external tools
**CNI**: k8s network communication (wavenet, calico, flannel)
**CSI**: communication with storage tools 

## 💡 Additional notes

* **Cluster HA:** not only the application, but k8s itself has to be resilient. For that, a production-level environment with at least 3 nodes of control plane is recommended.
* **Certifications:** CKAD is indicated for developers, while CKA is indicated for infrastructure professionals.

## 💻 Setup with k3d

It runs each node as a Docker container.

* **Minikube:** havier and creates complete VM.
* **Kind:** highly replicable for being yaml based.
* **K3d:** focus in CLI, pratical and fast for creating and destroying clusters.

Configuration of `kubectl` with cluster -> `~/.kube/config`. Contains credentials, addressing etc.
