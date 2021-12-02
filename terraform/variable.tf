variable "region" {
  type = string
}
variable "vpc_id" {
  type = string
}
variable "pub_subnet" {
  type = list(string)
}

variable "priv_subnet" {
  type = list(string)
}

variable "ec2_key" {
  type = string
}
variable "project" {
  type    = string
  default = "Lab"
}
variable "env" {
  type    = string
  default = "dev"
}

locals {
  tags = {
    Terraform = "true"
    Project   = "${var.project}"
  }
}