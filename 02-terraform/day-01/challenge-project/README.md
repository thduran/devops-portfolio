[english below]

# **Criando VPC na AWS via Terraform**

### **1. Credenciais**

* **Criação de usuário IAM:** deve ter as permissões necessárias pra que o Terraform gerenciE os recursos.

* **AWS CLI:** Pegue Access Key ID e Secret Access Key. Então, execute:
    ```bash
    aws configure
    ```
    Isso armazena as credenciais pra que o Terraform se autentique com a AWS.

### **2. Arquivos**

* `main.tf`: define versão e provider.
* `providers.tf`: define provider e região da AWS.
* `vpc.tf`: define recurso da VPC.

### **3. Execução**

1.  **`terraform plan`**: mostra quais recursos serão criados.
2.  **`terraform apply`**: aplica o plano e cria a infraestrutura.

**Resultado:** A criação da VPC foi executada com sucesso. Os arquivos de configuração utilizados estão no diretório atual.

---

[english]

# **Creating AWS VPC via Terraform**

### **1. Credentials**

* **Creation of IAM user:** it must have necessary permissions so Terraform can manage resources.

* **AWS CLI:** Get the Access Key ID and Secret Access Key. Then, run:
    ```bash
    aws configure
    ```
    It stores credentials so that Terraform can authenticate with AWS.

### **2. Files**

* `main.tf`: defines version and provider.
* `providers.tf`: defines provider and AWS region.
* `vpc.tf`: defines VPC resource.

### **3. Execution**

1.  **`terraform plan`**: shows what resources will be created.
2.  **`terraform apply`**: applies tha plan and creates the infrastructure.

**Result:** The VPC creation was executed with success. The configuration files are in the current directory.