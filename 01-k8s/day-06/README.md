[english below]

# **Projeto Kubenews - deploy com kind e na nuvem**

Containerização e deploy de uma aplicação web. O projeto base foi obtido a partir de um fork do repositório [Kube-News](https://github.com/KubeDev/kube-news).

---

## **1. Configuração e deploy local com kind**

1.  **Containerização:**
    * Adicionado um `Dockerfile` na pasta `/src` para construir a imagem.
    * Adicionado  `.dockerignore` para otimizar o build.

2.  **Criação do cluster local:**
    * Criado arquivo `kind-config.yaml` para definir a configuração do cluster local, incluindo port binding.
    * Executado comando para criar o cluster `kind`:
      ```bash
      kind create cluster --name mycluster --config kind-config.yaml
      ```

3.  **Criação dos manifestos:**
    * Criada pasta `k8s`.
    * Criado apenas um arquivo `k8s/deployment.yaml` para:
        * `deployment` e `service` do BD (PostgreSQL).
        * `deployment` e `service` da aplicação web.

4.  **Aplicação dos manifestos:**
    * Aplicados os manifestos para criar os recursos:
      ```bash
      kubectl apply -f k8s/deployment.yaml
      ```

5.  **Teste de conexão com BD:**
    * Utilizado `port-forward` para expor a porta do serviço PostgreSQL localmente. O teste teve sucesso com DBeaver.
      ```bash
      kubectl port-forward service/postgresql 5432:5432
      ```

6.  **Acesso:**
    * Com o `port binding` configurado no `kind-config.yaml` e o `service` da aplicação definido como `NodePort`, a aplicação ficou acessível em `http://localhost:30000`.

---

## **2. Deploy na nuvem (Digital Ocean)**

* **Mudança no Service:** tipo `NodePort` não é o ideal para expor serviços na nuvem. Foi alterado o `service` do app:
    * Removida a linha `nodePort: 30000`.
    * Troca `type: NodePort` para `type: LoadBalancer`.

* **Verificação do deploy:**
    1.  Após aplicar o manifesto atualizado, verificamos o status "running" dos pods:
        ```bash
        kubectl get po
        ```
    2.  Listamos os serviços para obter o IP do `LoadBalancer`:
        ```bash
        kubectl get svc
        ```

A aplicação foi exibida com sucesso.

---

## **3. Desafio: externalizar variáveis de ambiente**:

Remover as variáveis de ambiente (dados sensíveis do BD) que estavam hardcoded no `deployment.yaml`.

* **Solução:** Utilizamos `Secrets` do Kubernetes para armazenar esses dados.

    1.  Os valores das variáveis de ambiente (`DB_USER`, `DB_PASSWORD`, etc.) foram encriptados para o formato **base64**.
    2.  Criado novo arquivo `secret.yaml` para armazenar esses valores codificados.
    3.  O `deployment.yaml` foi ajustado para referenciar as chaves do `secret.yaml`.

* **Exemplo no `deployment.yaml`:**
    ```yaml
    - name: DB_DATABASE
      valueFrom:
        secretKeyRef:
          name: db-secret         # nome do Secret
          key: DB_DATABASE_CONFIG # chave dentro do Secret que contém o valor
    ```

---

[english]

# **Project Kubenews - deploy with kind and in cloud provider**

Containerization and deploy of web app. The base project was got from repo [Kube-News](https://github.com/KubeDev/kube-news).

---

## **1. Configuration and local deploy with kind**

1.  **Containerization:**
    * Added `Dockerfile` in directory `/src` to build the image.
    * Added  `.dockerignore` to optimize build.

2.  **Creation of local cluster:**
    * Created `kind-config.yaml` to define local cluster configuration, includind port binding.
    * Commando to create `kind` cluster:
      ```bash
      kind create cluster --name mycluster --config kind-config.yaml
      ```

3.  **Creation of manifests:**
    * Created `/k8s`.
    * Created just one `k8s/deployment.yaml` to:
        * `deployment` and `service` of DB (PostgreSQL).
        * `deployment` and `service` of web app.

4.  **Aplication of manifests:**
    * Manifests applied to create resources:
      ```bash
      kubectl apply -f k8s/deployment.yaml
      ```

5.  **Test of connection with BD:**
    * `port-forward` used to locally expose PostgreSQL service port. Test was succeded with DBeaver.
      ```bash
      kubectl port-forward service/postgresql 5432:5432
      ```

6.  **Access:**
    * With `port binding` set in `kind-config.yaml` and the application `service` set as `NodePort`, the application became acessible at `http://localhost:30000`.

---

## **2. Deploy in cloud provider (Digital Ocean)**

* **Change in service:** type `NodePort` it's not the ideal for exposing services in the cloud. `service` of app was changed.
    * Removed line `nodePort: 30000`.
    * Changed `type: NodePort` to `type: LoadBalancer`.

* **Deploy check:**
    1.  After applying the updated manifest, we could check status "running" pods:
        ```bash
        kubectl get po
        ```
    2.  Services listed to obtain `Loadbalancer` IP:
        ```bash
        kubectl get svc
        ```

The application was displayed with success.

---

## **3. Challenge: externalize environment variables**:

Remove environment variables (DB sensitive data) that was hardcoded in `deployment.yaml`.

* **Solutio:** `Secrets` used to storage these data.

    1.  The values of the environment variables (`DB_USER`, `DB_PASSWORD` etc.) were encrypted to **base64** format.
    2.  A new `secret.yaml` was created to store these coded values.
    3.  `deployment.yaml` was foi ajusted to reference the `secret.yaml` keys.

* **Exemple in `deployment.yaml`:**
    ```yaml
    - name: DB_DATABASE
      valueFrom:
        secretKeyRef:
          name: db-secret         # secret name
          key: DB_DATABASE_CONFIG # key inside the secret that contains the value
    ```