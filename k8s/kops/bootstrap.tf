terraform {
  required_version = ">= 0.12, < 0.14"
}

provider "aws" {
  region = var.AWS_REGION

  # Allow any 2.x version of the AWS provider
  version = "~> 2.0"
}

# variable "AWS_ACCESS_KEY" {}
#
# variable "AWS_SECRET_KEY" {}

variable "AWS_REGION" {
  default = "ap-southeast-2"
}

variable "PATH_TO_PRIVATE_KEY" {
  default = "mykey"
}

variable "PATH_TO_PUBLIC_KEY" {
  default = "mykey.pub"
}

variable "AMIS" {
  type = map(string)
  default = {
    us-east-1 = "ami-13be557e"
    us-west-2 = "ami-06b94666"
    eu-west-1 = "ami-844e0bf7"
    ap-southeast-2 = "ami-0dd7583b0a983a748"
  }
}

resource "aws_key_pair" "mykey" {
  key_name   = "mykey"
  public_key = file(var.PATH_TO_PUBLIC_KEY)
}

resource "aws_instance" "bootstrap" {
  ami           = var.AMIS[var.AWS_REGION]
  instance_type = "t2.micro"
  key_name      = aws_key_pair.mykey.key_name
  # vpc_security_group_ids = [aws_default_security_group.default.id]

}
#
# resource "aws_default_vpc" "default" {}
#
# resource "aws_default_security_group" "default" {
#   vpc_id      = aws_default_vpc.default.id
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   ingress {
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
# }

output "ip" {
  value = aws_instance.bootstrap.public_ip
}
