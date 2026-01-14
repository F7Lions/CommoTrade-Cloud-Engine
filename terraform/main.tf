terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67.0"  # STABLE DRIVER
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

# 1. VPC - Downgraded to v4.0.0 to match the Stable Driver
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "4.0.2" 

  name = "commotrade-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["ap-southeast-1a", "ap-southeast-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# 2. EKS - Pinned to v19.15 (Known "Golden" Version)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3" 

  cluster_name    = "commotrade-cluster"
  cluster_version = "1.30"
  
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    general = {
      min_size     = 1
      max_size     = 2
      desired_size = 1
      instance_types = ["t3.medium"]
    }
  }
}