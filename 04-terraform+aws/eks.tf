resource "aws_eks_cluster" "eks_cluster" { # creates control plane
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn # allows EKS to manage VPC

  vpc_config {
    subnet_ids             = module.vpc.public_subnets # set the network of the control plane
    endpoint_public_access = true # allows outside access (for kubectl, github actions)
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy, # the cluster is created only after eks_cluster_policy role is attached
  ]
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks_cluster.name # links to eks_cluster resource above
  node_group_name = "${var.cluster_name}-workers"
  node_role_arn   = aws_iam_role.eks_node_role.arn # see ./iam.tf
  subnet_ids      = module.vpc.public_subnets # set the network of the worker nodes. See line 6.

  instance_types = [var.instance_type]

  scaling_config {
    desired_size = var.node_desired_size
    max_size     = var.node_max_size    
    min_size     = var.node_min_size     
  }

  depends_on = [ # so that the node is not created before these 3 roles are attached
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ec2_container_registry_readonly,
  ]
}