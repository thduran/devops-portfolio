[english below]

# **Terraform com Digital Ocean**

Aqui resumo os principais blocos, conceitos, comandos do Terraform pra provisionar uma infraestrutura na Digital Ocean.

---

## **Tipos de blocos no Terraform**

### **1. Terraform settings**

Configurações do próprio Terraform no projeto, como a versão e os providers.

```hcl
terraform {
  required_version = ">1.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.16.0"
    }
  }
}
```

### **2. Providers**

Define cloud provider a ser utilizado e como se autenticar.

```hcl
provider "digitalocean" {
  token = "xxx"
}
```

### **3. Resources**

Recurso/elemento de infraestrutura que se deseja criar ou gerenciar (ex: VM, firewall).

```hcl
resource "digitalocean_droplet" "maquina_labs_tf" {
  image  = "ubuntu-20-04-x64"
  name   = "maquina-labs-tf"
  region = "nyc-1"
  size   = "s-1vcpu-2gb"
}
```

### **4. Data source**

Recurso que não foi criado pelo Terraform, mas que fará parte do projeto. Ex. vincular chave SSH já existente no novo Droplet (VM) ou uma subrede já existente que desejamos usar no projeto.

```hcl
data "digitalocean_ssh_key" "minha_chave" {
  name = "aula"
}
```

### **5. Variables**

Criação de variáveis para reutilizar em outras partes do código, tornando os manifestos mais dinâmicos e fáceis de manter.

```hcl
variable "regiao" {
  type        = string
  default     = "nyc-1"
  description = "Região de uso na Digital Ocean"
}
```

### **6. Outputs**

Usado para extrair/exibir informações sobre a infraestrutura após a criação, como o IP de uma VM.

```hcl
output "droplet_ip" {
  value = digitalocean_droplet.maquina_labs_tf.ipv4_address
}
```

* Exemplo de output pós terraform apply:
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
Outputs:
droplet_ip = "192.81.217.95"

* `terraform output`permite consultá-los a qualquer momento

---

## Provisionando VM e firewall na Digital Ocean

### a) Via web

### **1. Criar e adicionar chave SSH**

```bash
# Gera par de chaves
ssh-keygen -t rsa -b 2048

# Exibe chave pública para copiá-la
cat id_rsa.pub
```

* Cole em Settings > Security > Add SSH key.

### **2. Criar um Droplet (VM)**

* Droplet > Create.
* Selecione região, SO etc.
* Em Auth, escolha a chave adicionada.
* Defina hostname > Create.
* Copie o IP e acesse:

```bash
ssh -i ~/.ssh/id_rsa root@***.***.***.**
```

### **Criar e testar firewall**

* Network > Firewall > Create
* Defina inbound rules e associe ao Droplet criado.
* Para testar: Remover inbound rule SSH e tente acessar a máquina novamente. A conexão deve falhar, provando que o firewall está funcionando.

### b) Via Terraform

### Estrutura dos Arquivos

* `main.tf`: arquivo principal. Declaração dos elementos de infraestrutura (VM, firewall etc.).
* `terraform.tfstate`: armazena o estado atual da infraestrutura no cloud provider.
* Consulte a documentação do provedor da Digital Ocean: registry.terraform.io.

---

## Comandos Terraform

* `terraform init` Inicializa o projeto. Baixa os provedores necessários e prepara o ambiente para a execução.

* `terraform fmt` Formata o código dos seus arquivos .tf para seguir as convenções de estilo padrão, melhorando a legibilidade.

* `terraform validate` Verifica se a sintaxe do seu código Terraform está correta, sem checar o estado da infraestrutura.

* `terraform plan` Cria um plano de execução. Ele compara o estado desejado (seu código) com o estado atual (no arquivo .tfstate) e mostra o que será criado, alterado ou destruído.

* `terraform apply` Executa o plano de ação gerado pelo plan, provisionando ou modificando a infraestrutura. Use --auto-approve para pular a confirmação manual.

* `terraform destroy` Destrói todos os recursos de infraestrutura que foram criados e são gerenciados pelo Terraform neste projeto.

---

[english]

# **Terraform with Digital Ocean**

Here I summarize the main blocks, concepts, commands of Terraform to provision an infrasstructure in Digital Ocean.

---

## **Types de blocks in Terraform**

### **1. Terraform settings**

Configurations of Terraform itself in the project, such as version and providers.

```hcl
terraform {
  required_version = ">1.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.16.0"
    }
  }
}
```

### **2. Providers**

Define the cloud provider to be used and how to authenticate.

```hcl
provider "digitalocean" {
  token = "xxx"
}
```

### **3. Resources**

Resource/element of desired infrastructure to be create/managed (ex: VM, firewall).

```hcl
resource "digitalocean_droplet" "maquina_labs_tf" {
  image  = "ubuntu-20-04-x64"
  name   = "maquina-labs-tf"
  region = "nyc-1"
  size   = "s-1vcpu-2gb"
}
```

### **4. Data source**

Resource that wasn't created by Terraform, but will be part of the project. Ex. link existing SSH key to new Droplet (VM) or an existing subnet we want to use in the project.

```hcl
data "digitalocean_ssh_key" "my_key" {
  name = "aula"
}
```

### **5. Variables**

Creation of variables to be reutilized in other parts of the code, making manifests more dynamic and easy to keep.

```hcl
variable "region" {
  type        = string
  default     = "nyc-1"
  description = "Region of use in Digital Ocean"
}
```

### **6. Outputs**

Used to extract/display informations about the infrastructure after the creation, like the IP of a VM.

```hcl
output "droplet_ip" {
  value = digitalocean_droplet.maquina_labs_tf.ipv4_address
}
```

* Exemple of output after terraform apply:
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
Outputs:
droplet_ip = "192.81.217.95"

* `terraform output`can be used to check them anytime

---

## Provisioning VM and firewall in Digital Ocean

### a) Via web

### **1. Create and add SSH key**

```bash
# Generates key pair
ssh-keygen -t rsa -b 2048

# Displays public key to copy it
cat id_rsa.pub
```

* Paste in Settings > Security > Add SSH key.

### **2. Create a Droplet (VM)**

* Droplet > Create.
* Select region, OS etc.
* In Auth, select the added key.
* Define hostname > Create.
* Copy the IP and access:

```bash
ssh -i ~/.ssh/id_rsa root@***.***.***.**
```

### **Create and test firewall**

* Network > Firewall > Create
* Define the inbound rules and link it to the created Droplet.
* Testing: Remove SSH inbound rule and try to access the machine again. The connection should fail, proving the firewall is working.

### b) Via Terraform

### Files

* `main.tf`: main file. Definition of elements of infrastructure (VM, firewall etc.).
* `terraform.tfstate`: stores the current state of the infrastructure in the cloud provider.
* Check the documentation of Digital Ocean provider: registry.terraform.io.

---

## Terraform commands

* `terraform init` Initializes the project. Downloads the necessary providers and prepares the environment for execution.

* `terraform fmt` Formats the code of .tf files in order to follow standard style conventions of, improving readability.

* `terraform validate` Check if the Terraform code syntax is correct, without checking infrastructure state.

* `terraform plan` Creates an execution plan. It compares the desired state (the code) with the current state ().tfstate) e displays what's going to be created, updated ou destroyed.

* `terraform apply` Executes the action plan, provisioning or modifying the infrastructure. Use --auto-approve to skip manual confirmation.

* `terraform destroy` Destroys all resources created/managed by Terraform.