data "aws_availability_zones" "available" { # tells Terraform we want it to...
  state = "available"                       # return only the available AZs.
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.5.3"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr  # defines the main block of IPs for the whole VPC
  azs             = slice(data.aws_availability_zones.available.names, 0, 2) # get the list of AZs found by the block above and uses only the first 2 AZs. It ensures the VPC is multiregional, but limits it to 2 AZs.
  
  public_subnets  = var.public_subnets_cidr # defines what IP blocks to use for the public subnets
  private_subnets = [] # no private subnets created to simplify the project (not recommended in production-level).
  enable_nat_gateway  = false # since we don't...
  single_nat_gateway  = false # have private subnets.

  map_public_ip_on_launch = true # a public IP is automatically set to any instance created.

  public_subnet_tags = { # adds tags to the public subnets - mandatory for EKS.
    "kubernetes.io/cluster/${var.cluster_name}" = "shared" # for the control plane know it can use these subnets
    "kubernetes.io/role/elb"                      = "1" # for Kubernetes know these subnets are public and can be used to create ELBs
  }
}

# module internal outputs, so eks.tf can use them
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnets
}