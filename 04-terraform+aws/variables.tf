variable "cluster_name" {
  description = "Name to be used for the EKS cluster."
  type        = string
}

variable "aws_region" {
  description = "Region of AWS the resources are created."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets_cidr" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"] # defines blocks inside the VPC CIDR
}

variable "instance_type" {
  description = "Instance type for the nodes."
  type        = string
}

variable "node_desired_size" {
  description = "Desired number of nodes"
  type        = number
}

variable "node_max_size" {
  description = "Maximum number of nodes"
  type        = number
}

variable "node_min_size" {
  description = "Minimum number of nodes."
  type        = number
}