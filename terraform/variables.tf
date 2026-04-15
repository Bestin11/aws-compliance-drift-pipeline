variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix for all resource names"
  type        = string
  default     = "compliance-pipeline"
}

variable "alert_email" {
  description = "Email address to receive compliance alerts"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account ID used for S3 bucket naming"
  type        = string
}

variable "environment" {
  description = "Deployment environment label"
  type        = string
  default     = "dev"
}