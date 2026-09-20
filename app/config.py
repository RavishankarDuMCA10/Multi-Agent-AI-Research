import os
import socket
import boto3
import json
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_secret() -> dict:
    region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId="research-agent/config")
    return json.loads(response["SecretString"])


class Config:
    def __init__(self):
        data = _load_secret()

        # AWS
        self.aws_region: str = data.get("AWS_REGION", "us-east-1")

        # Bedrock Guardrails
        self.bedrock_guardrails_id: str = data["BEDROCK_GUARDRAILS_ID"]
        self.bedrock_guardrails_version: str = data["BEDROCK_GUARDRAILS_VERSION"]

        # Storage
        self.redis_url: str = data["REDIS_URL"]
        self.databse_url: str = data["DATABASE_URL"]
        self.tensorzero_url: str = data["TENSORZERO_URL"]
