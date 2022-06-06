data "aws_route53_zone" "selected" {
  name         = "rfexpert.net"
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = "www.rfexpert.net"
  type    = "A"

  alias {
    name                   = aws_lb.my-alb.dns_name
    zone_id                = aws_lb.my-alb.zone_id
    evaluate_target_health = true
  }
}


output "ns-servers" {
  value = data.aws_route53_zone.selected.name_servers
}
