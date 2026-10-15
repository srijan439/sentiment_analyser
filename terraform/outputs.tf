output "instance_id" {
  description = "ID of the sentiment-test EC2 instance."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "Public IPv4 address of the EC2 instance."
  value       = aws_instance.app.public_ip
}

output "application_url" {
  description = "URL for the Streamlit sentiment application."
  value       = "http://${aws_instance.app.public_ip}:8501"
}

output "ssh_command" {
  description = "Example command to connect using the configured EC2 key pair."
  value       = "ssh -i <path-to-${var.key_pair_name}.pem> ec2-user@${aws_instance.app.public_ip}"
}
