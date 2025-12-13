[english below]

### Services

Usamos `port-forward` (útil pra debugging) mas esse não é o modo habitual, temos que trabalhar com `services`, que são o ponto de comunicação externa ou interna entre pods. É possível usar IPs, mas não é uma boa prática pois IPs são voláteis (devido ao pod ser volátil), então usamos `services`.

---

### Tipos de services

1. ClusterIP: expõe os pods apenas internamente

```bash
# Aplica o deployment e service
kubectl apply -f deployment.yaml

# Lista services e mostra IP interno
kubectl get svc
```

2. NodePort: expõe o pod/service externamente, mas para acessar, é preciso ter o IP de algum dos pods. E em relação à porta do pod, esse tipo de service a escolhe aleatoriamente, entre 30000 e 32767.

```bash
# O tipo foi alterado para NodePort
kubectl apply -f deployment.yaml

# Mostra a porta mapeada (ex: 80:31614/TCP)
kubectl get svc
```

3. LoadBalancer: cria um IP público com balancedor de carga; usado só com k8s gerenciado de cloud provider.

4. ExternalName: serviço pra acessar serviços externos ou internos. Aponta pra um domínio para acessar  um BD, por exemplo, em vez de usar o endereço do BD direto.

### Endpoints e EndpointSlices

## Endpoints

Toda vez que `selector` é utilizado e pods são vinculados ao `service`, um `endpoint` pra cada pod são criados automaticamente.

* Consiste do IP do pod + porta do pod
* É uma das formas de verificar se existe um ponto de conexão entre service e pod.
    * Para testar isso, alterei o `selector` do deployment para um nome errado, apliquei e executei o comando abaixo: a `label` não tinha endpoints, pois nenhum pod tinha tal nome como label.

```bash
# Lista os endpoints com seus IPs/portas
kubectl get endpoints
```

**Dica** para debugging: se há problema de acesso ao pod via `service`, é importante verificar se o `endpoint` foi realmente criado com o comando acima.

## Endpointslice

A lista de IPs do cluster é dividida em "fatias" menores. Assim, quando um Pod muda, apenas a fatia menor correspondente é atualizada, tornando as atualizações muito mais rápidas e eficientes em grande escala.

---

## Comandos

### Teste de comunicação interna

1. Criando pod de teste (não gerenciado):
```bash
kubectl run prompt -it --image ubuntu -- /bin/bash`
```
2. Pegue o IP de um dos pods:
```bash
kubectl get po -o wide`
```
3. Dentro do pod de teste, acesse via IP (demonstra teste ok):
```bash
curl http://10.42.1.31
```
4. Como mencionado, não é boa prática. Então, acessamos via nome do service, para automaticamente usar LB.
```bash
curl http://serviceName
```

---

### Acessando NodePort externamente - caminho mais longo

1. Pegar o ID de um container
```bash
docker container ls
```

2. Pegar o IP
```bash
docker container inspect 910a77c612bc
```

3. Acessar
```bash
curl http://172.20.0.2:31614    # antes, kubectl get svc pra pegar a porta
```

---

### Caminho correto com port binding

1. Adicione a linha `nodePort: 30000` no yaml. Aplique e execute o comando abaixo pra verificar que a porta 30000 já foi definida.
```bash
kubectl get nodes
```

2. Recrie o cluster com port binding
```bash
k3d cluster create mycluster --servers 3 --agents 3 -p "30000:30000@loadbalancer"
```

3. Para ver o port binding
```bash
docker container ls
```

4. Agora o service pode ser acessado externamente
```bash
http://localhost:30000
```

No caso, foi 80:30000 (80 para interno, 30000 para externo).
Para testar, criei um pod não gerenciado novamente e executei `curl serviceName:30000` que não funcionou pois 30000 é pra externo. Já `curl serviceName:80` funcionou.

---

[english]

### Services

We used `port-forward` (useful for debugging), but this isn't the common usage. We have to work with `services`, that are the external ou internal point of communication between pods. It's possible to use IPs, but it isn't a best practice, because IPs are volatile (due to pod is volatile), so we use `services`.

---

### Types of services

1. ClusterIP: exposes pods only internally

```bash
# Applies deployment and service
kubectl apply -f deployment.yaml

# Lists services and show internal IP
kubectl get svc
```

2. NodePort: exposes pod/service externally, but to access it, to have the IP of one of the pods it's needed. In relation to the pod port, this type of service chooses it randomly, between 30000 and 32767.

```bash
# The type was changed to NodePort
kubectl apply -f deployment.yaml

# Shows the mapped port (ex: 80:31614/TCP)
kubectl get svc
```

3. LoadBalancer: creates a public IP with load balancer; used only with managed k8s of cloud providers.

4. ExternalName: service to access internal or external servieces. It points to o DB domain, for example, instead of using the DB address directly.

### Endpoints and EndpointSlices

## Endpoints

Every time a `selector` is used and pods are linked to the `service`, an `endpoint` for each pod is created automatically.

* It consists of the pod IP + pod port
* It's a way to check if there is an existing point of connection between `service` and pod.
    * To test it, I changed the deployment `selector` to a wrong name, applied it e run the following command: there weren't corresponding `endpoint` for the `label`, because no pod had this wrong name as `label`.

```bash
# Lists endpoints with their IPs/ports
kubectl get endpoints
```

**Tip** for debugging: if there's a pod access issue via `service`, it's important to check with the command above if the `endpoint` was actually created.

## Endpointslice

The list of cluster's IPs is split in smaller "slices". So, when a pod changes, only the smaller slice is updated, making updates much faster and efficient in large scale.

---

## Commands

### Test of internal communication

1. Creating test pod (non managed):
```bash
kubectl run prompt -it --image ubuntu -- /bin/bash`
```
2. Taking the IP of a pod:
```bash
kubectl get po -o wide`
```
3. Inside the test pod, access via IP (demonstrates test ok):
```bash
curl http://10.42.1.31
```
4. As mentioned, it's not a best practice. We must access via service name, so that the LB is automatically used.
```bash
curl http://serviceName
```

---

### Accessing NodePort externally - longer way

1. Take the ID of a container
```bash
docker container ls
```

2. Take the IP
```bash
docker container inspect 910a77c612bc
```

3. Access
```bash
curl http://172.20.0.2:31614    # before, kubectl get svc to take the port
```

---

### Correct way with port binding

1. Add line `nodePort: 30000` in the yaml file. Apply it and run the following command to verify that port 30000 is already set.
```bash
kubectl get nodes
```

2. Recreate the cluster with port binding
```bash
k3d cluster create mycluster --servers 3 --agents 3 -p "30000:30000@loadbalancer"
```

3. To see port binding
```bash
docker container ls
```

4. Now, the service can be accessed externally
```bash
http://localhost:30000
```

In this case, 80:30000 (80 for internal access, 30000 para external).
To test, I created a non-managed pod again and run `curl serviceName:30000` which didn't work, because 30000 is for external access. But `curl serviceName:80` worked.