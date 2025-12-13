[english below]

### Pods e containers

* **Pod**: menor unidade, onde os containers são executados.
    * É recomendado ter **1 container por pod** pra que cada container possa ser escalado individualmente.
* **Sidecar**: container auxiliar que atende a requisitos não funcionais, como coleta de logs. Executado junto ao container principal no mesmo Pod.

---

### yaml

* **Arquivos yaml**: arquivos de definição usados pra criar objetos (pods, deployments, services etc.) no Kubernetes.
* **`apiVersion`**: indica a versão da API do Kubernetes pro objeto que está sendo criado.
    * **Comando útil**: Para listar todas as APIs disponíveis, use `kubectl api-resources`.

### Escalabilidade e resiliência

* **Replicaset**: define a quantidade de réplicas desejadas de um Pod.
* **Importância**: sem `replicaset`, o cluster não terá escalabilidade, nem resiliência - se um pod falhar, ele não será recriado.

---

### Interação entre objetos

* **Labels e selectors**: chaves-valor. Definem quais objetos vão interagir entre si.
* **Atualização de pods**: sem um deployment, após aplicar um yaml num `replicaset` já existente (pra mudar a imagem do container, por exemplo), **é preciso apagar os pods antigos manualmente** para forçar o `replicaset` a criar pods atualizados.

---

## Comandos

### Pods

| Comando | Descrição |
| :--- | :--- |
| `kubectl apply -f pod.yaml` | cria ou atualiza o objeto |
| `kubectl get pods` | lista todos os pods |
| `kubectl get all` | lista todos os recursos |
| `kubectl get po -l app=web` | Lista pods filtrando com label |
| `kubectl describe pod mypod` | exibe eventos, status |
| `kubectl delete -f pod.yaml` | exclui o que foi definido no yaml |

### Replicasets

| Comando | Descrição |
| :--- | :--- |
| `kubectl get replicaset` | lista todos os replicasets |
| `kubectl apply -f replicaset.yaml && watch 'kubectl get rs,po'` | aplica o rs e monitora a criação para ver a resiliência. |
| `kubectl delete pod myreplicaset-ddrjx` | exclui um Pod para testar a resiliência |

### Acesso

| Comando | Descrição |
| :--- | :--- |
| `kubectl port-forward pod/mypod 8080:80` | encaminha a porta `80` do Pod `mypod` pra porta `8080` do host |
| `kubectl port-forward pod/myreplicaset-qn7d8 8080:80` | para um Pod específico |

---

[english]

### Pods and containers

* **Pod**: smallest unity, where containers are run.
    * It's recommended to have **1 container per pod** so that each container can be escalated individually.
* **Sidecar**: auxiliar container used for non-functional requirements, like log collection. It's run with the main container in the same pod.

---

### yaml

* **yaml files**: definition files used to create objects (pods, deployments, services etc.) in Kubernetes.
* **`apiVersion`**: indicates API version of Kubernetes for the object that is being created.
    * **Useful command**: To list all available APIs, run `kubectl api-resources`.

### Scalability and resilience

* **Replicaset**: defines how many replicas of pods we desire.
* **Importância**: without `replicaset`, the cluster won't have scalability, nor resilience - if a pod fails, it won't be recreated.

---

### Interaction between objects

* **Labels and selectors**: key-values. Define what objects will interact with each other.
* **Pod update**: without `deployment`, after applying a yaml to a existing `replicaset` (for example, to change the image), we need to **delete the old pods manually**, to force `replicaset` to create updated pods.

---

## Commands

### Pods

| Command | Description |
| :--- | :--- |
| `kubectl apply -f pod.yaml` | creates or update objects |
| `kubectl get pods` | lists all pods |
| `kubectl get all` | lists all resources |
| `kubectl get po -l app=web` | lists pods using lable filter |
| `kubectl describe pod mypod` | shows events, status |
| `kubectl delete -f pod.yaml` | deletes what the yaml "created" |

### Replicasets

| Command | Description |
| :--- | :--- |
| `kubectl get replicaset` | lists all replicasets |
| `kubectl apply -f replicaset.yaml && watch 'kubectl get rs,po'` | applies the rs and monitors creation to test resilience |
| `kubectl delete pod myreplicaset-ddrjx` | deletes a pod to test a resilience |

### Access

| Commando | Description |
| :--- | :--- |
| `kubectl port-forward pod/mypod 8080:80` | maps port `80` of pod `mypod` to port `8080` of host |
| `kubectl port-forward pod/myreplicaset-qn7d8 8080:80` | for a specific pod |