variable "do_token" {
  type        = string         # added
  description = "DO API token" # added
}

variable "droplet_name" {
  default     = "vm-tf"
  type        = string                 # added
  description = "Initial droplet name" # added
}

variable "droplet_region" {
  default     = "nyc1"
  type        = string            # added
  description = "Infra DO region" # added
}

variable "droplet_size" {
  default     = "s-1vcpu-2gb"
  type        = string             # added
  description = "Size of droplets" # added
}

variable "ssh_key_name" {
  default     = "thkey"
  type        = string    # added
  description = "SSH key" # added
}

# added
variable "vms_count" {
  default     = 1
  type        = number
  description = "Number of VMs"
}