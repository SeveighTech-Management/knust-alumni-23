import os

import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

BUCKET_NAME = os.environ.get("AWS_BUCKET")
CLOUDFRONT_DOMAIN = os.environ.get("CLOUDFRONT_DOMAIN")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("BUCKET_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("BUCKET_SECRET_ACCESS_KEY"),
)

my_config = Config(
    region_name=os.environ.get("AWS_BUCKET_REGION_NAME"),
    retries={
        "max_attempts": 10,
    },
)


def s3_client():
    session = boto3.session.Session()
    client = session.client(
        "s3",
        aws_access_key_id=os.environ.get("BUCKET_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("BUCKET_SECRET_ACCESS_KEY"),
        config=my_config,
    )
    return client


def send_files(file, file_key, file_type):
    client = s3_client()
    upload_file_response = client.put_object(
        Body=file, Bucket=BUCKET_NAME, Key=file_key, ContentType=file_type
    )
    return upload_file_response


def get_files(folder_slash_filename: str):
    url = f"{CLOUDFRONT_DOMAIN}/{folder_slash_filename}"

    return url
