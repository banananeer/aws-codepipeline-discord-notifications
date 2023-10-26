

# Example
```terraform
module "codepipeline_discord_notifications" {
  source = "git@github.com:banananeer/aws-codepipeline-discord-notifications.git//terraform"
  vpc_subnet_ids = module.vpc.private_subnets
  discord_webhook_url = "https://my-webhook"
}
```