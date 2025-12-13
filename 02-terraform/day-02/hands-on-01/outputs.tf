# displays IP after VM creation 
output "droplet_ip" {
  value = digitalocean_droplet.vm_aula[*].ipv4_address # line changed
}