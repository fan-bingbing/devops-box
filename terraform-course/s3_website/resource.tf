
resource "aws_s3_bucket" "b" {
  bucket = "s3-website.rfexpert.net"
  acl    = "public-read"
  policy = file("policy.json")

  website {
    index_document = "index.html"
    # error_document = "error.html"
    
  }

  tags = {
    Environment = "Prod"
  }
}


