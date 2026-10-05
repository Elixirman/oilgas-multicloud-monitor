output "vpc_id" {
  value = aws_vpc.hq_vpc.id
}

output "public_subnet_ids" {
  value = aws_subnet.hq_public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.hq_private[*].id
}

output "alb_security_group_id" {
  value = aws_security_group.alb_sg.id
}

output "pod_security_group_id" {
  value = aws_security_group.pod_sg.id
}

output "api_security_group_id" {
  value = aws_security_group.api_sg.id
}
