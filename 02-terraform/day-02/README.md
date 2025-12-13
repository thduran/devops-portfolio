[english below]

## Variables -> ./variables

* **Referência rápida:** [Documentação do Provedor `local`](https://registry.terraform.io/providers/hashicorp/local/latest/docs)

* **Exemplo básico com `local_file`:**
    Recurso `local_file` é usado para criar arquivos locais. O arquivo foi criado automaticamente após a execução do `terraform apply`.

    ```hcl
    resource "local_file" "foo" {
      content  = "conteúdo do arquivo"
      filename = "${path.module}/foo.bar"
    }
    ```

**Tipos de variáveis:**
    O arquivo `main.tf` neste diretório contém exemplos de cada tipo, como `list`, `map`, `number` etc.

* **Passando variáveis externamente:**
    É possível passar variáveis para o Terraform de várias maneiras:
    * Como **variável de ambiente** no terminal (ex: `export TF_VAR_nome_da_variavel="valor"`).
    * Utilizando a flag **`-var-file`** para especificar um arquivo de variáveis (ex: `terraform apply -var-file="testing.tfvars"`).
    * Utilizando a flag **`-var`** para passar uma variável diretamente na linha de comando.

---

## Meta-arguments -> ./meta-args

São configurações especiais que podem ser usadas com qualquer recurso para alterar seu comportamento.

* **`depends_on`**: Usado para criar uma dependência explícita entre recursos, garantindo que um recurso só seja criado após o outro.

* **`count`**: Permite criar um número específico de cópias de um recurso dinamicamente.

* **`for_each`**: Cria múltiplos recursos a partir de um `map` ou `set`, permitindo uma configuração mais flexível e nomeada do que o `count`.

*Todos os exemplos de uso estão demonstrados nos arquivos `.tf` deste diretório.*

---

## Hands-on

### **hands-on-01**

* É uma versão melhorada e refatorada de `day-01/classroom-project`.
* As mudanças possibilitam criação dinâmica de várias VMs, bastando definir a quantidade no `.tfvars`.
* *Toda linha adicionada/alterada está explicitamente demonstrada nos comentários dos arquivos Terraform.*

---

### **hands-on-02**

* É uma refatoração do `day-01/challenge-project`, aplicando melhores práticas de organização de código.
* **Refatoração:**
    * Valores fixos (nome da VPC e região da AWS) foram separados no `variables.tf`.
    * Criado `.tfvars` para popular as variáveis, separando a configuração da lógica.
    * Criado `outputs.tf` para exibir o ARN da VPC após a criação.

* **Exemplo de Saída:**
    ```
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    Outputs:
    vpc_arn = "arn:aws:ec2:us-east-1:035386953677:vpc/vpc-00e4d6d3d1dfead0b"
    ```

---

### **hands-on-03**

* Provisiona instância EC2 t2.micro na AWS.
* Utiliza variables pra definir o tipo de instância (`instance_type`) e o ID da imagem (`AMI`), tornando a configuração flexível.

**Exemplo de saída:**
    ```
    aws_instance.best-ec2: Creating...
    aws_instance.best-ec2: Still creating... [00M10s elapsed]
    aws_instance.best-ec2: Creation complete after 14s [id=i-0ed41751367f6e3d5]
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

---

[english]

## Variables -> ./variables

* **Quick reference:** [Documentation of `local` provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)

* **Basic example with `local_file`:**
    Resource `local_file` is used to create local files. The file was automatically created after execution of `terraform apply`.

    ```hcl
    resource "local_file" "foo" {
      content  = "file content"
      filename = "${path.module}/foo.bar"
    }
    ```

**Types of variables:**
    File `main.tf` in this directory has examples of each type, ad `list`, `map`, `number` etc.

* **Defining variables externally:**
    It's possible to set variables to Terraform in many ways:
    * As **environmente variable** on the terminal (ex: `export TF_VAR_variable_name="value"`).
    * Using flag **`-var-file`** to specify a file of variables (ex: `terraform apply -var-file="testing.tfvars"`).
    * Using flag **`-var`** to set a variable directly by the CLI.

---

## Meta-arguments -> ./meta-args

They are special configurations that can be use with any resource to change its behavior.

* **`depends_on`**: Used to create an explicit dependency between resources, ensuring that one resource is only created after another.

* **`count`**: allows you to create a specific number of copies of a resource dynamically.

* **`for_each`**: Creates multiple resources from a `map` or `set`, allowing a more flexible and named configuration than `count`.

*All examples are demonstrated in `.tf` files in this directory deste diretório.

---

## Hands-on

### **hands-on-01**

* It's a better and refactored version of `day-01/classroom-project`.
* The changes allow dynamic creation of several VMs,  mudanças possibilitam criação dinâmica de várias VMs, simply defining the quantity in `.tfvars`.
* *Every added/changed line is explicitly demonstrated in the comments inside Terraform files.*

---

### **hands-on-02**

* Refactoration of `day-01/challenge-project`, applying best practices of coding.
* **Refatoração:**
    * Fixed values (VPC name and AWS region) were separated in `variables.tf`.
    * `.tfvars` created to set the variable content, separation configuration from logic.
    * `outputs.tf` created to display VPC ARN after creation.

* **Output example:**
    ```
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    Outputs:
    vpc_arn = "arn:aws:ec2:us-east-1:035386953677:vpc/vpc-00e4d6d3d1dfead0b"
    ```

---

### **hands-on-03**

* Provisions EC2 t2.micro instance in AWS.
* Uses variables to set instance type (`instance_type`) and image ID (`AMI`), making configuration flexible.

**Output example:**
    ```
    aws_instance.best-ec2: Creating...
    aws_instance.best-ec2: Still creating... [00M10s elapsed]
    aws_instance.best-ec2: Creation complete after 14s [id=i-0ed41751367f6e3d5]
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```