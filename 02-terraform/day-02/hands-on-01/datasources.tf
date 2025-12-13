# registry.terraform.io/providers/digitalocean/digitalocean/latest/docs > data sources
data "digitalocean_ssh_key" "ssh_key" {
  name = var.ssh_key_name
}