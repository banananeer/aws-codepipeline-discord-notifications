resource "aws_sqs_queue" "this" {
  name                        = "codepipeline-discord-notifications.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.this_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "this_dlq" {
  name                        = "codepipeline-discord-notifications-dlq.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

resource "aws_sqs_queue_policy" "this" {
  queue_url = aws_sqs_queue.this.id
  policy    = data.aws_iam_policy_document.queue.json
}