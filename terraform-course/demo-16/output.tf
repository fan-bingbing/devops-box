output "LB" {
  value = aws_lb.my-alb.dns_name
}

# output "rds" {
#   value = aws_db_instance.mariadb.endpoint
# }
