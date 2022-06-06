output "ip" {
  value = aws_eip.example-eip.public_ip
}

# output "rds" {
#   value = aws_db_instance.mariadb.endpoint
# }

# output "ELB" {
#   value = aws_elb.my-elb.dns_name
# }
