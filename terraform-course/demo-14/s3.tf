resource "aws_s3_bucket" "b" {
  bucket = "mybucket-c29df11265xyd"
  acl    = "private"

  tags = {
    Name = "mybucket-c29df11265xyd"
  }
}
