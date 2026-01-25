import os
import uuid
import logging
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(file_bytes: bytes, filename: str = None) -> str | None:
    """
    Upload file bytes to S3 and return the S3 path.

    Returns the S3 path (key) on success, or None on failure.
    """
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    if not bucket_name:
        logging.error("S3_BUCKET_NAME environment variable is not set.")
        return None

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
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
        logging.info(f"Successfully uploaded to S3: {s3_key}")
        return s3_key
    except ClientError as e:
        logging.error(f"Failed to upload to S3: {e}")
        return None
