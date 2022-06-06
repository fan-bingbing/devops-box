variable "AWS_REGION" {
  default = "ap-southeast-2"
}

variable "AMIS" {
  type = map
  default = {
    ap-southeast-2 = "ami-0dd7583b0a983a748"
  }
}

variable "PATH_TO_PRIVATE_KEY" {
  default = "mykey"
}

variable "PATH_TO_PUBLIC_KEY" {
  default = "mykey.pub"
}
