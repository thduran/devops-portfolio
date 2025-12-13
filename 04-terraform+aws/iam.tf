# file responsible for create identities (roles) and give them permissions (policies) so that the AWS services can interact
# ---

resource "aws_iam_role" "eks_cluster_role" { # role creation
  name_prefix = "eks-cluster-role-${var.cluster_name}-" # prevents error EntityAlreadyExists (409)

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole" # grants permission to...
        Effect    = "Allow"          # assume role.
        Principal = { Service = "eks.amazonaws.com" } # defines who can assume this role
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" { # defines what policies the role above will have
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy" # gives EKS permission to manage network resources
  role       = aws_iam_role.eks_cluster_role.name
}

# ---

resource "aws_iam_role" "eks_node_role" { # second role - for the nodes
  name_prefix = "eks-node-role-${var.cluster_name}-" # prevents error EntityAlreadyExists (409)

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "ec2.amazonaws.com" } # defines that only EC2 service can assume this role
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy" # allows kubelet to access control plane and get status.
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy" # so that the node can manage the network inside the cluster and communicate with CNI
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "ec2_container_registry_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly" # allows the node to authenticate in ECR and pull container images
  role       = aws_iam_role.eks_node_role.name
}