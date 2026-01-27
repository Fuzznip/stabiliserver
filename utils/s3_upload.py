import os
import uuid
import logging
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file_bytes: bytes, filename: str = None) -> str | None:
    """
    Upload file bytes to S3 and return the full object URL.

    Returns the full S3 URL on success, or None on failure.
    """
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    region = os.environ.get("AWS_REGION", "us-east-1")
    if not bucket_name:
        logging.error("S3_BUCKET_NAME environment variable is not set.")
        return None

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region
    )

    # Generate a unique filename if not provided
    if not filename:
        filename = f"{uuid.uuid4()}.png"
    else:
        # Ensure uniqueness by prepending UUID
        filename = f"{uuid.uuid4()}_{filename}"

    s3_key = f"loot/{filename}"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=file_bytes,
            ContentType="image/png"
        )
        object_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
        logging.info(f"Successfully uploaded to S3: {object_url}")
        return object_url
    except ClientError as e:
        logging.error(f"Failed to upload to S3: {e}")
        return None
