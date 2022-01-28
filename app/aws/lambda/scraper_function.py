import os
import shutil

import boto3
from dotenv import load_dotenv

from ..constant import (
    EVENTS_SCHEDULER_RULE,
    LAMBDA_IAM_ROLE_NAME,
    RUNTIME,
    SOCIAL_MEDIA_PLATFORMS,
)

# Load environment variables
load_dotenv()


def create_crawler_lambda_functions():
    zip_crawler_scripts()
    create_functions()
    create_scheduler_rule()
    scheduler_put_targets()
    create_scheduler_trigger()


def zip_crawler_scripts():
    """
    Zip all the daily scraper scripts for each social media platform.
    To be uploaded to their respective AWS Lambda function.
    """
    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:
            shutil.make_archive(
                base_name=f"./app/aws/lambda/{platform}",
                format="zip",
                root_dir=f"./app/scraper/{platform}",
                base_dir="daily.py",
            )
        except Exception as e:
            print(e)

        print(f"daily scraper script for {platform} is zipped successfully.")


def create_functions():
    """
    Creates the crawler AWS Lambda function for each social media platform

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


def create_scheduler_rule():
    """
    Creates a daily schedule rule in AWS EventBridge
    """
    events_client = boto3.client("events")
    try:
        events_client.put_rule(
            Name=EVENTS_SCHEDULER_RULE,
            ScheduleExpression="rate(1 day)",
            State="ENABLED",
            RoleArn=f"arn:aws:iam::{os.getenv('AWS_ACCOUNT_ID')}:role/{LAMBDA_IAM_ROLE_NAME}",
        )
    except Exception as e:
        print(e)


def scheduler_put_targets():
    """
    Creates event target (each social media platform) for AWS EventBridge daily schedule rule
    """
    events_client = boto3.client("events")

    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:
            events_client.put_targets(
                Rule=EVENTS_SCHEDULER_RULE,
                Targets=[
                    {
                        "Id": f"Events_add_target_{platform}",
                        "Arn": f"arn:aws:lambda:{os.getenv('AWS_REGION')}:{os.getenv('AWS_ACCOUNT_ID')}:function:{platform}_scheduled_crawler",
                    }
                ],
            )
        except Exception as e:
            print(e)

        print(f"Target {platform} succesfully added to scheduler event.")


def create_scheduler_trigger():
    """
    Creates an AWS EventBridge daily schedule rule trigger for each social media platform
    """
    lambda_client = boto3.client("lambda")

    for platform in SOCIAL_MEDIA_PLATFORMS:
        try:
            lambda_client.add_permission(
                FunctionName=f"arn:aws:lambda:{os.getenv('AWS_REGION')}:{os.getenv('AWS_ACCOUNT_ID')}:function:{platform}_scheduled_crawler",
                StatementId="DailyScheduleTriggerRule",
                Action="lambda:InvokeFunction",
                Principal="events.amazonaws.com",
                SourceArn=f"arn:aws:events:{os.getenv('AWS_REGION')}:{os.getenv('AWS_ACCOUNT_ID')}::rule/{EVENTS_SCHEDULER_RULE}",
            )
        except Exception as e:
            print(e)

        print(f"Scheduler trigger is successfully added to {platform}.")
