resource "aws_cloudwatch_event_rule" "this" {
  name        = "codepipeline-events"
  description = "Capture each AWS Codepipeline Event"

  event_pattern = jsonencode({
    source = [
      "aws.codepipeline"
    ],
    "$or": [
      {
        "detail-type": [
          "CodePipeline Action Execution State Change",
          "CodePipeline Stage Execution State Change"
        ],
        "detail": {
          "state": ["FAILED"]
        }
      },
      {
        "detail-type": ["CodePipeline Pipeline Execution State Change"],
        "detail": {
          "state": ["STARTED", "SUCCEEDED", "FAILED"]
        }
      }
    ]
  })
}

resource "aws_cloudwatch_event_target" "this" {
  rule      = aws_cloudwatch_event_rule.this.name
  target_id = "send-to-discord-notification-queue"
  arn       = aws_sqs_queue.this.arn

  sqs_target {
    message_group_id = "codepipeline-events"
  }
}

data "aws_cloudwatch_event_bus" "default" {
  name = "default"
}