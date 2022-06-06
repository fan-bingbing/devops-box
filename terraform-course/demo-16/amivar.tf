data "aws_ami" "selected" {
  owners           = ["self"]
  most_recent      = true
  # filter {
  #   name   = "name"
  #   values = ["myami *"]
  # }
}
