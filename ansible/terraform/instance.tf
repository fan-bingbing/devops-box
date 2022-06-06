resource "aws_key_pair" "mykey" {
  key_name   = "mykey"
  public_key = file(var.PATH_TO_PUBLIC_KEY)
}


resource "aws_instance" "u_workers" {
  ami           = "ami-0dd7583b0a983a748"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.mykey.key_name
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y nginx python
              EOF
}

resource "aws_instance" "c_workers" {
  ami           = "ami-05f50d9ec7e4c3b02"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.mykey.key_name
  user_data = <<-EOF
              #!/bin/bash
              yum update
              yum install -y python
              EOF
}

output "ip1" {
  value = aws_instance.u_workers.public_ip
}
output "ip2" {
  value = aws_instance.c_workers.public_ip
}
