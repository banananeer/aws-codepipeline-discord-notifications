import json
import os
from dataclasses import dataclass

import pytest


@pytest.fixture
def action_execution_state_change_json():
    with open("sample_events/codepipeline-action-execution-state-change.json") as phial:
        data = json.load(phial)

        sqs_event = {
            "Records": [
                {
                    "messageId": "11d6ee51-4cc7-4302-9e22-7cd8afdaadf5",
                    "receiptHandle": "AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...",
                    "body": json.dumps(data),
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1573251510774",
                        "SequenceNumber": "18849496460467696128",
                        "MessageGroupId": "1",
                        "SenderId": "AIDAIO23YVJENQZJOL4VO",
                        "MessageDeduplicationId": "1",
                        "ApproximateFirstReceiveTimestamp": "1573251510774",
                    },
                    "messageAttributes": {},
                    "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:fifo.fifo",
                    "awsRegion": "us-east-2",
                }
            ]
        }
        yield sqs_event


@pytest.fixture
def stage_execution_state_change_json():
    with open("sample_events/codepipeline-stage-execution-state-change.json") as phial:
        data = json.load(phial)
        sqs_event = {
            "Records": [
                {
                    "messageId": "11d6ee51-4cc7-4302-9e22-7cd8afdaadf5",
                    "receiptHandle": "AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...",
                    "body": json.dumps(data),
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1573251510774",
                        "SequenceNumber": "18849496460467696128",
                        "MessageGroupId": "1",
                        "SenderId": "AIDAIO23YVJENQZJOL4VO",
                        "MessageDeduplicationId": "1",
                        "ApproximateFirstReceiveTimestamp": "1573251510774",
                    },
                    "messageAttributes": {},
                    "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:fifo.fifo",
                    "awsRegion": "us-east-2",
                }
            ]
        }
        yield sqs_event


@pytest.fixture
def pipeline_execution_state_change_json():
    with open(
        "sample_events/codepipeline-pipeline-execution-state-change.json"
    ) as phial:
        data = json.load(phial)
        sqs_event = {
            "Records": [
                {
                    "messageId": "11d6ee51-4cc7-4302-9e22-7cd8afdaadf5",
                    "receiptHandle": "AQEBBX8nesZEXmkhsmZeyIE8iQAMig7qw...",
                    "body": json.dumps(data),
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1573251510774",
                        "SequenceNumber": "18849496460467696128",
                        "MessageGroupId": "1",
                        "SenderId": "AIDAIO23YVJENQZJOL4VO",
                        "MessageDeduplicationId": "1",
                        "ApproximateFirstReceiveTimestamp": "1573251510774",
                    },
                    "messageAttributes": {},
                    "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:fifo.fifo",
                    "awsRegion": "us-east-2",
                }
            ]
        }
        yield sqs_event


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = (
            "arn:aws:lambda:eu-west-1:123456789012:function:test"
        )
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return LambdaContext()


@pytest.fixture(autouse=True, scope="module")
def discord_webhook_url():
    return "http://discord-webhook"


@pytest.fixture(autouse=True)
def environment(discord_webhook_url):
    os.environ["DISCORD_WEBHOOK_URL"] = discord_webhook_url
