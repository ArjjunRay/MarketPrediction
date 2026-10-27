import json
from typing import Any

import boto3  # type: ignore[import-untyped]
import structlog

from app.core.config import get_settings
from app.core.logging import configure_logging

logger = structlog.get_logger(__name__)


def ensure_object_storage() -> None:
    """Create the local research bucket and prove that S3 reads/writes work."""
    settings = get_settings()
    client: Any = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
    )
    existing = {item["Name"] for item in client.list_buckets().get("Buckets", [])}
    if settings.s3_bucket not in existing:
        client.create_bucket(Bucket=settings.s3_bucket)

    key = "_health/bootstrap.json"
    payload = json.dumps({"service": "qstream", "status": "ok"}).encode()
    client.put_object(Bucket=settings.s3_bucket, Key=key, Body=payload)
    stored = client.get_object(Bucket=settings.s3_bucket, Key=key)["Body"].read()
    if stored != payload:
        raise RuntimeError("S3-compatible storage round-trip returned different bytes")
    client.delete_object(Bucket=settings.s3_bucket, Key=key)
    logger.info("object_storage_ready", bucket=settings.s3_bucket)


if __name__ == "__main__":
    configure_logging(get_settings().log_level)
    ensure_object_storage()
