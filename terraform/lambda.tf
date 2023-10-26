# Create zip-archive of a single directory where "poetry export" & "pip install --no-deps" will also be executed (not using docker)


module "lambda" {
  source          = "terraform-aws-modules/lambda/aws"
  function_name   = "codepipeline-discord-notifications"
  create_function = true

  runtime = "python3.9"
  handler = "index.handler"

  source_path = [
    {
      path           = "${path.module}/../"
      poetry_install = true
      patterns = [
        "!tests/.*",
        "!terraform/.*",
        "!.git/.*",
        "!.idea/.*",
        "!.__pycache__/.*",
        "!.gitignore",
        "!pyproject.toml",
        "!poetry.toml",
        "!.pre-commit-config.yaml",
      ]
    }
  ]
  artifacts_dir = "${path.root}/builds/codepipeline-discord-notifications/"

  event_source_mapping = {
    sqs = {
      event_source_arn = aws_sqs_queue.this.arn
    }
  }

  allowed_triggers = {
    sqs = {
      principal  = "sqs.amazonaws.com"
      source_arn = aws_sqs_queue.this.arn
    }
  }

  create_current_version_allowed_triggers = false

  attach_network_policy = true
  vpc_subnet_ids = var.vpc_subnet_ids

  environment_variables = {
    DISCORD_WEBHOOK_URL = var.discord_webhook_url
  }

  attach_policy_json = true
  policy_json        = data.aws_iam_policy_document.lambda.json
}