terraform {
    required_version = ">= 1.3.7"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
}

# Configure AWS Provider
provider "aws" {
    profile = "reddit-pipeline-profile"
    region = var.aws_region
}



# Create S3 bucket
resource "aws_s3_bucket" "data-pipeline-bucket" {
  bucket = var.s3_bucket
  force_destroy = true
}


# S3 bucket object_ownership
resource "aws_s3_bucket_ownership_controls" "data-pipeline-bucket-control" {
  bucket = aws_s3_bucket.data-pipeline-bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}


# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_data-pipeline-bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.data-pipeline-bucket-control]
  bucket = aws_s3_bucket.data-pipeline-bucket.id
  acl    = "private"
}

# Create S3 read & write access role. This is assigned to Redshift cluster so that it can read data from S3. Write access needed for unloading data back to S3t
resource "aws_iam_role" "redshift_role" {
  name = "prod_redshift_role"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3FullAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

# Create security group for Redshift allowing all inbound/outbound traffic
 resource "aws_security_group" "sg_redshift" {
  name        = "sg_redshift"
  ingress {
    description = "all traffic"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    description = "all traffic"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# Configure redshift cluster. 
resource "aws_redshift_cluster" "redshift" {
  cluster_identifier = "data-pipeline-redshift"
  skip_final_snapshot = true
  master_username    = "awsuser"
  master_password    = var.redshift_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = "true"
  iam_roles = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.sg_redshift.id]
}
