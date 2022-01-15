import os 
from dotenv import load_dotenv
import json
import boto3
from ..exception import AwsBucketCreationError
from ..utils import aws_utils

# Load environment variables
load_dotenv()

# Constants
SOCIAL_MEDIA_PLATFORMS = [
    "reddit",
    "instagram",
    "facebook",
    "youtube",
    "twitter"
]

############################ AWS S3 SETUP ############################

# Establish s3 client
client = boto3.client('s3')

# Create buckets for project
try:
    for platform in SOCIAL_MEDIA_PLATFORMS:
        bucket_name = f"smt483tls-{platform}-bucket"
        bucket_response = aws_utils.create_s3_bucket(client=client, bucket_name=bucket_name)

        # if bucket_response['HTTPStatusCode'] > 299:
        #     raise AwsBucketCreationError(BUCKET_NAME)

        # Create s3 bucket policy 
        policy = aws_utils.create_s3_policy_object(bucket_name=bucket_name)
        bucket_policy = json.dumps(policy)
        policy_response = aws_utils.create_bucket_policy(
            client=client, 
            bucket_name=bucket_name, 
            policy=bucket_policy
        )

        # if policy_response['HTTPStatusCode'] > 299:
        #     raise AwsBucketCreationError(BUCKET_NAME)
except Exception as e:
    print(e)


############################ AWS DYNAMODB SETUP ############################
