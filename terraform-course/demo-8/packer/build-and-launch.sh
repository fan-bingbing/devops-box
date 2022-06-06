#!/bin/bash


AMI_ID=$(packer build )
echo 'variable "AMI_ID" { default = "'${AMI_ID}'" }' > ../amivar.tf

# terraform apply
