import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import (
    EventBridgeEvent,
    event_source,
    SQSEvent,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from discord_webhook import DiscordWebhook

logger = Logger()

client = boto3.client("sqs", region_name=os.environ.get("AWS_REGION"))


def create_action_execution_message(detail: dict):
    message = f"Pipeline {detail['pipeline']} stage {detail['stage']} action {detail['action']} {detail['state']}"
    return message


def create_stage_execution_message(detail: dict):
    message = f"Pipeline {detail['pipeline']} stage {detail['stage']} {detail['state']}"
    return message


def create_pipeline_execution_message(detail: dict):
    message = f"Pipeline {detail['pipeline']} {detail['state']}"
    return message


@logger.inject_lambda_context
@event_source(data_class=SQSEvent)
def handler(event: SQSEvent, context: LambdaContext) -> str:
    for record in event.records:
        eventbridge_event = EventBridgeEvent(record.json_body)
        print(eventbridge_event.__dict__)
        if "action" in eventbridge_event.detail:
            logger.info(f"Processing action execution event.")
            message = create_action_execution_message(eventbridge_event.detail)
        elif "stage" in eventbridge_event.detail:
            logger.info(f"Processing stage execution event.")
            message = create_stage_execution_message(eventbridge_event.detail)
        else:
            logger.info(f"Processing pipeline execution event.")
            message = create_pipeline_execution_message(eventbridge_event.detail)

        webhook = DiscordWebhook(
            url=os.environ.get("DISCORD_WEBHOOK_URL"), content=message
        )
        webhook.execute()

        client.delete_message(
            ReceiptHandle=record.receipt_handle, QueueUrl=record.queue_url
        )

    return "done"
