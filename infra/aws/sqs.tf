resource "aws_sqs_queue" "image_processing_queue" {
  name                      = "plant-photo-processing"
  delay_seconds             = 0
  message_retention_seconds = 86400 # 1 day
  receive_wait_time_seconds = 10
}

output "sqs_url" {
  value = aws_sqs_queue.image_processing_queue.id
}