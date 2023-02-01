# Output Region set for AWS
output "aws_region" {
    description = "Region set for AWS"
    value = var.aws_region
}

# Output bucket name
output "s3_bucket_name" {
    description = "Bucket name"
    value = var.s3_bucket
}

# Output Redshift hostname
output "redshift_cluster_hostname" {
  description = "ID of the Redshift instance"
  value       = replace(
      aws_redshift_cluster.redshift.endpoint,
      format(":%s", aws_redshift_cluster.redshift.port),"",
  )
}

# Output Redshift port
output "redshift_port" {
    description = "Port of Redshift cluster"
    value = aws_redshift_cluster.redshift.port
}

# Output Redshift role
output "redshift_role" {
    description = "Role assigned to Redshift"
    value = aws_iam_role.redshift_role.name
}
