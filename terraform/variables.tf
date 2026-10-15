variable "project_name" {
  description = "Name for the EC2 instance and security group."
  type        = string
  default     = "sentiment-test"
}

variable "aws_region" {
  description = "AWS region where EC2 will be created."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance size. t3.large is selected for the BERT model's memory use."
  type        = string
  default     = "t3.large"
}

variable "docker_image" {
  description = "Public Docker Hub image and tag, for example dockerhub-user/sentiment-bert:latest."
  type        = string

  validation {
    condition     = can(regex("^[^/]+/[^:]+:[^:]+$", var.docker_image))
    error_message = "Use a Docker Hub image in namespace/repository:tag format, such as username/sentiment-bert:latest."
  }
}

variable "key_pair_name" {
  description = "Name of an EC2 key pair in the selected AWS region."
  type        = string
  default     = "nimbus-key"
}

variable "ssh_allowed_cidr" {
  description = "Your public IPv4 address with /32, for example 203.0.113.10/32."
  type        = string

  validation {
    condition     = can(cidrnetmask(var.ssh_allowed_cidr)) && can(regex("/32$", var.ssh_allowed_cidr))
    error_message = "Set ssh_allowed_cidr to your public IPv4 address followed by /32."
  }
}
