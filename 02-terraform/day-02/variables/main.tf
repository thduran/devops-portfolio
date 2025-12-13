resource "local_file" "foo" {
  # content  = var.conteudo  # references the variable below
  # content = var.conteudo2
  # content = var.conteudo3
  # content = "The machine I'm gonna use is ${var.conteudo4[1]}"
  # content = "The machine I like is type ${var.conteudo5["small"]}"
  # content = "My setup options are ${join(", ",var.conteudo6)}"
  # content = "My choices are ${var.conteudo7.regiao} - ${var.conteudo7.opcao_maquina} - ${var.conteudo7.fazer_bkp}"
  content  = "My choices are ${var.conteudo8[0]} - ${var.conteudo8[1]} - ${var.conteudo8[2]}"
  filename = "./arquivo.txt"
}

variable "conteudo8" {
  default = ["nyc3", "big", "true"]
  type    = tuple([string, string, bool])
}

variable "conteudo7" {
  default = {
    regiao        = "nyc1"
    opcao_maquina = "medium"
    fazer_bkp     = false
  }
  type = object({ regiao = string, opcao_maquina = string, fazer_bkp = bool }) # to join related values in one block
}

variable "conteudo6" {
  default     = ["s-1vcpu-2gb", "s-2vcpu-4gb", "s-4vcpu-8gb"]
  type        = set(string) # type set doesn't recognize repeated values, doesn't work with index and show values in random order
  description = "conteúdo que vai para o arquivo"
}

variable "conteudo5" {
  default = {
    "small"  = "s-1vcpu-2gb"
    "medium" = "s-2vcpu-4gb"
    "big"    = "s-4vcpu-8gb"
  }
  type        = map(string)
  description = "conteúdo que vai para o arquivo"
}

variable "conteudo4" {
  default     = ["machine 01", "machine 02"]
  type        = list(string)
  description = "conteúdo que vai para o arquivo"
}

variable "conteudo3" {
  default     = false
  type        = bool
  description = "conteúdo que vai para o arquivo"
}


variable "conteudo2" {
  default     = 1
  type        = string
  description = "conteúdo que vai para o arquivo"
}

variable "conteudo" {
  default     = "Conteúdo do arquivo"
  type        = string
  description = "conteúdo que vai para o arquivo"
}