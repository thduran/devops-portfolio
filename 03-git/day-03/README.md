[english below]

# **Pipeline CD com GitHub Actions e Kubernetes**

Descrevo o pipeline de CD `.github/workflows/first-workflow.yaml` (linhas 84 a 105), que faz deploy da aplicação em um cluster Kubernetes.

**Obs.** O código é o mesmo do diretório `day-02/`, copiados para `day-03/`. A diferença é o diretório `k8s` pro deploy.

---

## **Funcionamento**

* **Dependência:** A linha `needs: [CI]` garante que o job de CD só inicia após sucesso do job `CI`.

### **Passos:**

1.  **Configuração do contexto Kubernetes:**
    * Pra que o workflow possa interagir com o cluster Kubernetes, é preciso definir o `kubeconfig`.
    * **Action usada:** `azure/k8s-set-context@v4`.
    * **Segurança:** O conteúdo do arquivo `kubeconfig` é armazenado de forma segura como **secret**.
        * Para obter o `kubeconfig` localmente: `code ~/.kube/config`.
        * Na Digital Ocean, basta seguir as instruções iniciais deles, para setar localmente o `kubeconfig` e exibi-lo.
        * O conteúdo é colado no Github como secret.

2.  **Deploy**
    * O próximo passo é aplicar os manifestos Kubernetes.
    * **Action usada:** `Azure/k8s-deploy@v5`.

3.  **Verificação:**
    * Após conclusão do CD, você pode verificar o status do deploy e acessar a aplicação:
        * Execute `kubectl get svc` pra obter o IP externo do service.
        * Acesse o IP no navegador pra testar.

---

## **Workflow de teste adicional (`test-workflow.yaml`)**

Outro workflow (`test-workflow.yaml`) também foi criado pra demonstrar uma abordagem complementar da interação do Kubernetes com o Actions.

* **Configuração:**
    * Configura o `kubectl` no ambiente de execução (runner) do Actions.
    * Adiciona o `kubeconfig` (armazenado como secret) ao diretório `~/.kube/config` da VM do runner.
* **Ações:**
    * Usa `kubectl apply` pra aplicar os manifestos.
    * Usa `kubectl set image` pra garantir que o `deployment` use a nova imagem construída.

---

[english]

# **CD Pipeline with Actions and Kubernetes**

I describe the CD pipeline `.github/workflows/first-workflow.yaml` (lines 84 to 105), which deploys the application to a Kubernetes cluster.

**Note** The code is the same as in the `day-02/` directory, copied to `day-03/`. The difference is the `k8s` directory for deployment.

---

## **How it Works**

* **Dependency:** The line `needs: [CI]` ensures that the CD job only starts after the `CI` job succeeds.

### **Steps:**

1.  **Kubernetes context configuration:**
    * For the workflow to interact with the Kubernetes cluster, the `kubeconfig` needs to be defined.
    * **Action used:** `azure/k8s-set-context@v4`.
    * **Security:** The content of the `kubeconfig` file is stored securely as a **secret**.
        * To get the `kubeconfig` locally: `code ~/.kube/config`.
        * On Digital Ocean, just follow their initial instructions to set the `kubeconfig` locally and display it.
        * The content is pasted into Github as a secret.

2.  **Deploy**
    * The next step is to apply the Kubernetes manifests.
    * **Action used:** `Azure/k8s-deploy@v5`.

3.  **Verification:**
    * After the CD completes, you can check the deployment status and access the application:
        * Run `kubectl get svc` to get the external IP of the service.
        * Access the IP in the browser to test.

---

## **Additional test workflow (`test-workflow.yaml`)**

Another workflow (`test-workflow.yaml`) was also created to demonstrate a complementary approach to Kubernetes interaction with Actions.

* **Configuration:**
    * Configures `kubectl` in the Actions runner environment.
    * Adds the `kubeconfig` (stored as a secret) to the runner VM's `~/.kube/config` directory.
* **Actions:**
    * Uses `kubectl apply` to apply the manifests.
    * Uses `kubectl set image` to ensure the `deployment` uses the newly built image.