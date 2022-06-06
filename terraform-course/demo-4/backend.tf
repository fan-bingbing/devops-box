terraform {
  backend "s3" {
    bucket = "terraform-backend-jofe"
    key = "terraform/demo4"
  }
}
