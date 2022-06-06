provider "aws" {
  access_key = "AKIAQ677PCJ4N7QXKYFF"
  secret_key = "6QeHxpDrQYRRB7qak/4jZxHAMb4pnGUDuPpHbfEk"
  region     = "ap-southeast-2"
}

resource "aws_instance" "example" {
  ami           = "ami-099e6eeef1c3dac48"
  instance_type = "t2.micro"
}


# terraform plan, show changes it would make
# terraform apply
# terreform plan -out changes.tf && terraform apply changes.tf && rm changes.tf
# terraform destroy
