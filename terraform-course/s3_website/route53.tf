data "aws_route53_zone" "selected" {
  name         = "rfexpert.net"
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = "s3-website.rfexpert.net" # must be the same as the bucket name 
  type    = "A"

  alias {
    name    = aws_s3_bucket.b.website_domain
    zone_id = aws_s3_bucket.b.hosted_zone_id
    evaluate_target_health = true
  }
}


output "ns-servers" {
  value = data.aws_route53_zone.selected.name_servers
}

output "s3-endpoint" {
  value = aws_s3_bucket.b.website_endpoint
}

output "s3-domain" {
  value = aws_s3_bucket.b.website_domain
}