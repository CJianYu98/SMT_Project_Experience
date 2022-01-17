import os

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_s3_bucket(client: boto3.client, bucket_name: str) -> dict:
    """
    This function attempts to create a AWS S3 bucket with the given bucket name.

    Args:
        client (boto3.S3.client): Low-level client representing AWS S3
        bucket_name (str): Bucket name for the S3 bucket

    Returns:
    """
    return client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")},
    )


def create_s3_policy_object(bucket_name: str) -> dict:
    """
    To create policy object for AWS S3. To be converted to json format.

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
                "Principal": {
                    "AWS": [f"arn:aws:iam::{os.getenv('AWS_ACCOUNT_ID')}:root"]
                },
            }
        ],
    }


def create_bucket_policy(client: boto3.client, bucket_name: str, policy: str) -> dict:
    """
    To implement the policy for a AWS S3 bucket.

    Args:
        client (boto3.client): Low-level client representing AWS S3
        bucket_name (str): Bucket name for the S3 bucket
        policy (str): Policies for the S3 bucket

    Returns:
        dict: Response object
    """
    return client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
