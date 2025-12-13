[english below]

## **1. Definindo variáveis de ambiente direto no manifesto**

A forma mais simples de passar configurações para um container é através da seção `env` no manifesto do `deployment`.

* **Cenário de teste:**
    1.  Ao aplicar o `deployment.yaml` e acessar `localhost:30000`, utilizou as variáveis de ambiente padrão da imagem.
    2.  Então, ao adicionar `env` no manifesto, as variáveis padrão foram ignoradas e substituídas.

* **`deployment.yaml`:**
    ```yaml
    containers:
    - name: app-configuration
      image: kubedevio/app-variaveis-ambiente:v1
      ports:
      - containerPort: 3000
      env:
      - name: APP_NAME
        value: "My k8s app"
      - name: APP_VERSION
        value: "2.0"
      - name: APP_AUTHOR
        value: "Thiago Duran"
    ```

* **Vantagem:**
    * A imagem não precisa ser reconstruída para alterar as configurações.

* **Desvantagem:**
    * Mas os dados ficam visíveis diretamente no arquivo yaml, que não é uma boa prática.

Por isso, usamos `configMaps` e `secrets`.

## **2. Configmaps**

O `configmap` armazena em formato de chave-valor. Para dados não sensíveis, pois também ficam visíveis.

### **Vinculando `configMap` ao `deployment`**

* **Por referência (injeta todos os valores do configmap):**
    ```yaml
    # Remove a seção 'env' e adiciona 'envFrom'
    envFrom:
      - configMapRef:
          name: app-config # nome do configmap
    ```

* **Por valor (injeta um valor específico):**
    ```yaml
    env:
      - name: APP_NAME # nome da variável de ambiente no container
        valueFrom:
          configMapKeyRef:
            name: app-config # nome do configmap
            key: APP_NAME_CONFIG # chave dentro do configmap
    ```

## **3. Secrets**

Similar ao `configmap`, mas destinado a armazenar dados sensíveis. Os valores são armazenados em formato `base64`.

> Embora os dados não fiquem expostos diretamente, a codificação `base64` é facilmente reversível. É recomendado usar `secrets` junto com uma ferramenta externa de gerenciamento de chaves, como o Vault da HashiCorp.

* **Tipos:** `Opaque` (padrão), `kubernetes.io/service-account-token`, `kubernetes.io/dockercfg`, `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth`, `kubernetes.io/tls`.

### **Criando secrets**

* **Via CLI:**
    ```bash
    kubectl create secret generic secret-name --from-literal=VALUE_NAME="value"
    ```

* **Via manifesto:**
    1.  Primeiro, codificar o valor desejado em `base64`:
        ```bash
        echo -n "value" | base64
        ```
    2.  Copiar o valor e adicionar no `secret.yaml`.

---

## **Comandos**

### **Configmaps**

* **Listar configmaps:**
    ```bash
    kubectl get configmap
    ```
* **Criar configmap:**
    ```bash
    kubectl create configmap configmap-name --from-literal=VALUE_NAME="My k8s app"
    ```
* **Criar configmap passando arquivo:**
    ```bash
    kubectl create configmap configmap-name --from-literal=APP_NAME="My k8s app test" --from-literal=APP_VERSION="4.0" --from-file file.config
    ```
* **Inspecionar configmap:**
    ```bash
    kubectl describe configmap configmap-name
    ```
* **Criar configmap via manifesto:**
    ```bash
    kubectl apply -f configmap.yaml
    ```
* **Deletar configmap:**
    ```bash
    kubectl delete configmap configmap-name
    ```

### **Secrets**

* **Listar secrets:**
    ```bash
    kubectl get secrets
    ```
* **Inspecionar secret:**
    Mostra as informações do `Secret`, mas não expõe valores.
    ```bash
    kubectl describe secret app-secret
    ```
* **Visualizar e decodificar um secret (para fim de demonstração):**
    1.  Obtendo o yaml, o valor será mostrado em `base64`.
        ```bash
        kubectl get secret app-secret -o yaml
        ```
    2.  Copie e decodifique para ver o valor original.
        ```bash
        echo "TXkgdGVzdCBhcHAgMg==" | base64 -d
        ```

---

[english]

## **1. Defining environment variables in the manifest**

The simplest way to input configurations into a container is through `env` section in the `deployment` manifest.

* **Test scenario:**
    1.  When applying `deployment.yaml` and accessing `localhost:30000`, it utilized the default image env variables.
    2.  So, when adding `env` to the manifest, the default variables are ignored and replaced.

* **`deployment.yaml`:**
    ```yaml
    containers:
    - name: app-configuration
      image: kubedevio/app-variaveis-ambiente:v1
      ports:
      - containerPort: 3000
      env:
      - name: APP_NAME
        value: "My k8s app"
      - name: APP_VERSION
        value: "2.0"
      - name: APP_AUTHOR
        value: "Thiago Duran"
    ```

* **Pro:**
    * The image doesn't need to be rebuilt to change configurations.

* **Con:**
    * But, data is visible directly in the yaml file, not a best practice.

Because of that, we use`configmaps` and `secrets`.

## **2. Configmaps**

Stores data in key-value format. Used for non-sensible data, because they also become visible.

### **Linking `configMap` to `deployment`**

* **By reference (injects all configmap values):**
    ```yaml
    # Remove 'env' section and add 'envFrom'
    envFrom:
      - configMapRef:
          name: app-config # name of configmap
    ```

* **By value (injects specific value):**
    ```yaml
    env:
      - name: APP_NAME # environment variable name in the container
        valueFrom:
          configMapKeyRef:
            name: app-config # configmap name
            key: APP_NAME_CONFIG # key inside configmap
    ```

## **3. Secrets**

Similar to `configmap`, but it stores sensitive data. Values are stored in `base64` format.

> Although data are not expose directly, `base64` encryption is easily reversible. It's recommended to use `secrets` along with an external key management tool, like HashiCorp Vault.

* **Types:** `Opaque` (default), `kubernetes.io/service-account-token`, `kubernetes.io/dockercfg`, `kubernetes.io/basic-auth`, `kubernetes.io/ssh-auth`, `kubernetes.io/tls`.

### **Creating secrets**

* **Via CLI:**
    ```bash
    kubectl create secret generic secret-name --from-literal=VALUE_NAME="value"
    ```

* **Via manifest:**
    1.  First, encrypt desired value in `base64`:
        ```bash
        echo -n "value" | base64
        ```
    2.  Copy the value and add to `secret.yaml`.

---

## **Commands**

### **Configmaps**

* **List configmaps:**
    ```bash
    kubectl get configmap
    ```
* **Create configmap:**
    ```bash
    kubectl create configmap configmap-name --from-literal=VALUE_NAME="My k8s app"
    ```
* **Create configmap using file:**
    ```bash
    kubectl create configmap configmap-name --from-literal=APP_NAME="My k8s app test" --from-literal=APP_VERSION="4.0" --from-file file.config
    ```
* **Inspect configmap:**
    ```bash
    kubectl describe configmap configmap-name
    ```
* **Create configmap via manifest:**
    ```bash
    kubectl apply -f configmap.yaml
    ```
* **Delete configmap:**
    ```bash
    kubectl delete configmap configmap-name
    ```

### **Secrets**

* **List secrets:**
    ```bash
    kubectl get secrets
    ```
* **Inspect secret:**
    Shows information of the `secret`, but doesn't expose values.
    ```bash
    kubectl describe secret app-secret
    ```
* **Visualize e decode a secret (demonstration purposes):**
    1.  Getting o yaml, the value will be displayed in `base64`.
        ```bash
        kubectl get secret app-secret -o yaml
        ```
    2.  Copy and decode it to see original value.
        ```bash
        echo "TXkgdGVzdCBhcHAgMg==" | base64 -d
        ```
