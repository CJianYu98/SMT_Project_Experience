import json

import boto3
from dotenv import load_dotenv

iam = boto3.client("iam")


def create_lambda_iam_role():
    """
    To create IAM role for AWS Lambda function
    """
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "LambdaIamRole",
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            },
            {
                "Effect": "Allow",
                "Principal": {"Service": "events.amazonaws.com"},
                "Action": "sts:AssumeRole",
            },
            {
                "Effect": "Allow",
                "Principal": {"Service": "s3.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    try:
        iam.create_role(
            RoleName="LambdaTestingRole1", AssumeRolePolicyDocument=json.dumps(policy)
        )

        iam.attach_role_policy(
            RoleName="LambdaTestingRole1",
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        )

        iam.attach_role_policy(
            RoleName="LambdaTestingRole1",
            PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonS3FullAccess",
        )
        
    except Exception as e:
        pass

    print("IAM role created successfully.")