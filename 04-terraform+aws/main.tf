terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # protects from a major update above v6.0
    }
  }
}

provider "aws" {
  region = var.aws_region
}