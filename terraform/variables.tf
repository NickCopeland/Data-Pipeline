variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = ""
}

variable "s3_bucket" {
  description = "Bucket name"
  type        = string
  default     = ""
}

variable "redshift_password" {
  description = "Redshift user password"
  type        = string
  default     = ""
}