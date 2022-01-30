import json
import os

import boto3
import botocore.exceptions
from dotenv import load_dotenv

from ..constant import LAMBDA_IAM_ROLE_NAME

load_dotenv()

iam = boto3.client("iam")


def create_iam_role_permission_policy() -> str:
    """
    Creates AWS Lambda IAM Role permission policy which allow access to AWS CloudWatch, S3 and DynamoDB.

    Returns:
        str: Permission policy name. Used to permission policy name when attaching the policy to the AWS IAM Role.
    """
    try:
        permission_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                    "Resource": "*",
                },
                {"Effect": "Allow", "Action": ["s3:*", "s3-object-lambda:*"], "Resource": "*"},
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:BatchGetItem",
                        "dynamodb:GetItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:BatchWriteItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:GetRecords",
                    ],
                    "Resource": "*",
                },
            ],
        }

        permission_policy_name = "AWSLambdaBasicExecutionRoleAndAmazonS3FullAccess"
        iam.create_policy(
            PolicyName=permission_policy_name, PolicyDocument=json.dumps(permission_policy)
        )

        print(f">>> IAM role policy {permission_policy_name} created successfully.")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            print("Policy already exists/created, no further actions required.")
        else:
            print(e)

    return permission_policy_name


def create_lambda_iam_role(permission_policy_name: str):
    """
    To create IAM role for AWS Lambda functions.
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
            },
        ],
    }

    try:
        iam.create_role(RoleName=LAMBDA_IAM_ROLE_NAME, AssumeRolePolicyDocument=json.dumps(policy))

        iam.attach_role_policy(
            RoleName=LAMBDA_IAM_ROLE_NAME,
            PolicyArn=f"arn:aws:iam::{os.getenv('AWS_ACCOUNT_ID')}:policy/{permission_policy_name}",
        )
        print(f">>> IAM role {LAMBDA_IAM_ROLE_NAME} created successfully.")
    except Exception as e:
        print(e)
