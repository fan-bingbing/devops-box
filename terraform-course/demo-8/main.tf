resource "aws_instance" "example" {
  ami           = var.AMIS[var.AWS_REGION]
  instance_type = "t2.micro"

  # the VPC subnet
  subnet_id = aws_subnet.main-public-1.id

  # the security group
  vpc_security_group_ids = [aws_security_group.allow-ssh.id]

  # the public SSH key
  key_name = aws_key_pair.mykey.key_name

  provisioner "file" {
    source      = "script.sh"
    destination = "/tmp/script.sh"
  }
  provisioner "file" {
    source      = "nginx.service"
    destination = "/tmp/nginx.service"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mv /tmp/nginx.service /lib/systemd/system/nginx.service",
      "chmod +x /tmp/script.sh",
      "sudo sed -i -e 's/\r$//' /tmp/script.sh",  # Remove the spurious CR characters.
      "sudo /tmp/script.sh",
      "sudo systemctl start nginx",
      "sudo systemctl enable nginx"
    ]
  }
  connection {
    host        = coalesce(self.public_ip, self.private_ip)
    type        = "ssh"
    user        = var.INSTANCE_USERNAME
    private_key = file(var.PATH_TO_PRIVATE_KEY)
  }
}

# resource "aws_ebs_volume" "ebs-volume-1" {
#   availability_zone = "ap-southeast-2a"
#   size              = 20
#   type              = "gp2"
#   tags = {
#     Name = "extra volume data"
#   }
# }
#
# resource "aws_volume_attachment" "ebs-volume-1-attachment" {
#   device_name = "/dev/xvdh"
#   volume_id   = aws_ebs_volume.ebs-volume-1.id
#   instance_id = aws_instance.example.id
# }

# resource "aws_instance" "packer_build_example" {
#   ami           = var.AMI_ID
#   instance_type = "t2.micro"
#
#   # the VPC subnet
#   subnet_id = aws_subnet.main-public-1.id
#
#   # the security group
#   vpc_security_group_ids = [aws_security_group.allow-ssh.id]
#
#   # the public SSH key
#   key_name = aws_key_pair.mykey.key_name
# }

resource "aws_eip" "example-eip" {
  instance = aws_instance.example.id
  vpc = true
}
