variable "instance_type" {
  type        = string
  description = "Size of VM"
}

variable "aws_region" {
  type        = string
  description = "AWS region the resources will be created"
}

variable "ami_id" {
  type        = string
  description = "AMI ID for EC2 instance."
  default     = ""
}