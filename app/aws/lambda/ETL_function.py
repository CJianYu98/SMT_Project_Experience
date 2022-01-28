import os
import shutil

import boto3
from dotenv import load_dotenv

from ..constant import LAMBDA_IAM_ROLE_NAME, RUNTIME, SOCIAL_MEDIA_PLATFORMS

# Load environment variables
load_dotenv()


def create_etl_lambda_functions():
    zip_etl_scripts()
    create_functions()
    create_s3_trigger()


def zip_etl_scripts():
    """
    Zip all the ETL scripts for each social media platform.
    To be uploaded to their respective AWS Lambda function.
    """
    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:
            shutil.make_archive(
                base_name=f"./app/aws/lambda/etl/{platform}",
                format="zip",
                root_dir="./app/aws/lambda/etl",
                base_dir=f"{platform}.py",
            )

        except Exception as e:
            print(e)

        print(f"Daily scraper script for {platform} is zipped successfully.")


def create_functions():
    """
    Creates the ETL AWS Lambda function for each social media platform

    Args:
        iam_client (boto3.Client): AWS IAM Client
        lambda_client (boto3.Client): AWS Lambda Client
    """
    iam_client = boto3.client("iam")
    lambda_client = boto3.client("lambda")
    role = iam_client.get_role(RoleName=LAMBDA_IAM_ROLE_NAME)

    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:

            # Read zipped script into binary format
            with open(f"./app/aws/lambda/{platform}.zip", "rb") as f:
                crawler_code = f.read()

            lambda_client.create_function(
                FunctionName=f"{platform}_scheduled_crawler",
                Runtime=RUNTIME,
                Role=role["Role"]["Arn"],
                Handler="daily.lambda_handler",
                Code=dict(ZipFile=crawler_code),
                Timeout=300,  # Maximum allowable timeout
            )
        except Exception as e:
            print(e)

        print(f"AWS Lambda function was successfully created for {platform}.")


def create_s3_trigger():
    """
    Creates the S3 trigger for each ETL AWS Lambda function. It first creates an AWS Lambda permission then creates a notification its respective S3 bucket to complete the trigger creation.
    """
    lambda_client = boto3.client("lambda")
    s3_resource = boto3.resource("s3")

    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:
            # Adds S3 trigger permission
            function_name = f"{platform}_scheduled_crawler"
            lambda_client.add_permission(
                StatementId=f"S3_invoke_{function_name}",
                FunctionName=function_name,
                Action="lambda:InvokeFunction",
                Principal="s3.amazonaws.com",
                SourceArn=f"arn:aws:s3:::smt483tls-{platform}-bucket",
                SourceAccount=os.getenv("AWS_ACCOUNT_ID"),
            )

            # Create notification for object creation event in S3 bucket
            bucket_notification = s3_resource.BucketNotification(f"smt483tls-{platform}-bucket")
            bucket_notification.put(
                Bucket=f"smt483tls-{platform}-bucket",
                NotificationConfiguration={
                    "LambdaFunctionConfigurations": [
                        {
                            "LambdaFunctionArn": f'arn:aws:lambda:{os.getenv("AWS_REGION")}:{os.getenv("AWS_ACCOUNT_ID")}:function:{function_name}',
                            "Events": ["s3:ObjectCreated:*"],
                        }
                    ]
                },
            )
        except Exception as e:
            print(e)

        print(f"S3 trigger was successfully created for {platform}.")
