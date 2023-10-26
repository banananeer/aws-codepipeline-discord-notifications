import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.jmespath_utils import (
    extract_data_from_envelope,
    envelopes,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from discord_webhook import DiscordWebhook

logger = Logger()


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
def lambda_handler(event: dict, context: LambdaContext) -> str:
    records: list = extract_data_from_envelope(data=event, envelope=envelopes.SQS)
    for record in records:
        eventbridge_event = EventBridgeEvent(record)

        if "action" in eventbridge_event.detail:
            logger.info(f"Processing action execution event.")
            message = create_action_execution_message(eventbridge_event.detail)
        elif "stage" in eventbridge_event.detail:
            logger.info(f"Processing stage execution event.")
            message = create_stage_execution_message(eventbridge_event.detail)
        else:
            logger.info(f"Processing pipeline execution event.")
            message = create_pipeline_execution_message(eventbridge_event.detail)

    webhook = DiscordWebhook(url=os.environ.get("DISCORD_WEBHOOK_URL"), content=message)
    webhook.execute()

    return message
