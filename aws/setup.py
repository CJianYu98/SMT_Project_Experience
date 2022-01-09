import os 
from dotenv import load_dotenv
import json
import boto3

# Load environment variables
load_dotenv()

# Constants
BUCKET_NAME = 'smt483tls-proj-bucket'


############################ AWS S3 SETUP ############################

# Establish s3 client
client = boto3.client('s3')

# Create bucket for project
try:
    response = client.create_bucket(
        Bucket = BUCKET_NAME,
        CreateBucketConfiguration = {
            'LocationConstraint': os.getenv('AWS_REGION')
        }
    )

    # if response['HTTPStatusCode'] > 299:
    #     raise AwsBucketCreationError(BUCKET_NAME)
except Exception as e:
    print(e)

# Create s3 bucket policy
policy = {
    "Version": "2012-10-17",
    "Id": "Smt483-proj-bucket-policy",
    "Statement": [
        {
            "Sid": "Smt483-proj-bucket-policy1",
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*",
            "Principal": {
                "AWS": [
                    f"arn:aws:iam::{os.getenv('AWS_ACCOUNT_ID')}:root"
                ]
            }
        }
    ]
}
bucket_policy = json.dumps(policy)

try:
    response = client.put_bucket_policy(Bucket = BUCKET_NAME, Policy = bucket_policy)

    # if response['HttpStatusCode'] > 299:
    #     raise AwsBucketCreationError(BUCKET_NAME)
except Exception as e:
    print(e)


############################ AWS DYNAMODB SETUP ############################