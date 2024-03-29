import responses
from responses.matchers import json_params_matcher

from index import handler


def test_action_execution_state_change_notification(
    action_execution_state_change_json, lambda_context, discord_webhook_url, mocker
):
    mocker.patch("index.client.delete_message")
    responses.add(
        method=responses.POST,
        url=discord_webhook_url,
        json={"id": "webhook-id"},
        status=200,
        match=[
            json_params_matcher(
                {
                    "attachments": [],
                    "content": "Pipeline drf-lab-pipeline stage Build action Build SUCCEEDED",
                    "embeds": [],
                    "wait": True,
                }
            )
        ],
    )
    handler(action_execution_state_change_json, lambda_context)


def test_pipeline_execution_state_change_notification(
    pipeline_execution_state_change_json, lambda_context, discord_webhook_url, mocker
):
    mocker.patch("index.client.delete_message")
    responses.add(
        method=responses.POST,
        url=discord_webhook_url,
        json={"id": "webhook-id"},
        status=200,
        match=[
            json_params_matcher(
                {
                    "attachments": [],
                    "content": "Pipeline drf-lab-pipeline STARTED",
                    "embeds": [],
                    "wait": True,
                }
            )
        ],
    )
    handler(pipeline_execution_state_change_json, lambda_context)


def test_stage_execution_state_change_notification(
    stage_execution_state_change_json, lambda_context, discord_webhook_url, mocker
):
    mocker.patch("index.client.delete_message")
    responses.add(
        method=responses.POST,
        url=discord_webhook_url,
        json={"id": "webhook-id"},
        status=200,
        match=[
            json_params_matcher(
                {
                    "attachments": [],
                    "content": "Pipeline drf-lab-pipeline stage Build STARTED",
                    "embeds": [],
                    "wait": True,
                }
            )
        ],
    )
    handler(stage_execution_state_change_json, lambda_context)
