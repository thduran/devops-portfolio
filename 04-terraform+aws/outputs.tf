  output "cluster_name" {
    description = "EKS cluster name"
    value       = aws_eks_cluster.eks_cluster.name
  }

  output "cluster_endpoint" {
    description = "EKS endpoint (API server)."
    value       = aws_eks_cluster.eks_cluster.endpoint
  }

  output "configure_kubectl_command" {
    description = "Command to set kubeconfig locally"
    value       = "aws eks update-kubeconfig --name ${aws_eks_cluster.eks_cluster.name} --region ${var.aws_region}"
    
  }
