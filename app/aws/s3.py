import json
import os

import boto3
from dotenv import load_dotenv

from ..exception import AwsBucketCreationError
from .constant import SOCIAL_MEDIA_PLATFORMS

# Load environment variables
load_dotenv()


def s3_setup():
    """
    This function creates AWS S3 buckets for each of the social media platform to store raw data everyday.
    Bucket policy will be implemented for each S3 bucket.
    """

    client = boto3.client("s3")  # Establish s3 client

    try:
        for platform in SOCIAL_MEDIA_PLATFORMS:
            bucket_name = f"smt483tls-{platform}-bucket"
            bucket_response = client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")},
            )

            # if bucket_response['HTTPStatusCode'] > 299:
            #     raise AwsBucketCreationError(BUCKET_NAME)

            policy = create_s3_policy_object(bucket_name=bucket_name)
            bucket_policy = json.dumps(policy)
            policy_response = client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

            # if policy_response['HTTPStatusCode'] > 299:
            #     raise AwsBucketCreationError(BUCKET_NAME)
    except Exception as e:
        print(e)


def create_s3_policy_object(bucket_name: str) -> dict:
    """
    Create policy object for AWS S3 based on the template.

    Args:
        bucket_name (str): Bucket name for the S3 bucket

    Returns:
        dict: policy object
    """
    return {
        "Version": "2012-10-17",
        "Id": "Smt483-proj-bucket-policy",
        "Statement": [
            {
                "Sid": "Smt483-proj-bucket-policy1",
                "Action": "s3:*",
                "Effect": "Allow",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
                "Principal": {"AWS": [f"arn:aws:iam::{os.getenv('AWS_ACCOUNT_ID')}:root"]},
            }
        ],
    }
