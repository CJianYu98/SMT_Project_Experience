import boto3
import json
from dotenv import load_dotenv
from ..exception import AwsBucketCreationError
from ..utils import aws_utils
from .constant import SOCIAL_MEDIA_PLATFORMS

# Load environment variables
load_dotenv()

def s3_setup():
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
