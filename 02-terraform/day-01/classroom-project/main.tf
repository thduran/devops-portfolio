terraform {
  required_version = "~>1.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# creates VM (droplet): registry.terraform.io/providers/digitalocean/digitalocean/latest/docs > Droplets
resource "digitalocean_droplet" "vm_aula" {
  image    = "ubuntu-22-04-x64"
  name     = var.droplet_name                       # if changed, there's no downtime
  region   = var.droplet_region                     # if changed, there's downtine
  size     = var.droplet_size                       # check at: slugs.do-api.dev
  ssh_keys = [data.digitalocean_ssh_key.ssh_key.id] # links existing SSH key to the VM (datasources.tf)
}

# creates firewall: documentation > firewall
resource "digitalocean_firewall" "firewall-aula" {
  name = "firewall-aula"

  droplet_ids = [digitalocean_droplet.vm_aula.id] # links firewall to VM

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "53"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "22"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "80"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "443"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}