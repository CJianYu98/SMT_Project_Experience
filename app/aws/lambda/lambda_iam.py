import json

import boto3
from dotenv import load_dotenv

iam = boto3.client("iam")


def create_lambda_iam_role() -> dict:
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
        ],
    }

    try:
        response = iam.create_role(
            RoleName="LambdaTestingRole1", AssumeRolePolicyDocument=json.dumps(policy)
        )

        response1 = iam.attach_role_policy(
            RoleName="LambdaTestingRole1",
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        )

        response2 = iam.attach_role_policy(
            RoleName="LambdaTestingRole1",
            PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonS3FullAccess",
        )
        
    except Exception as e:
        pass

    return {"code": 200}
