# Import packages
import shutil
from logging.handlers import SocketHandler

import boto3

from ..constant import SOCIAL_MEDIA_PLATFORMS


def create_clients():
    iam_client = boto3.client("iam")
    lambda_client = boto3.client("lambda")
    s3_resource = boto3.resource("s3")
    role = iam_client.get_role(RoleName="LambdaTestingRole1")
    return iam_client, lambda_client, s3_resource, role

iam_client, lambda_client, s3_resource, role = create_clients()

# Zip scraping scripts for all platforms
for platform in SOCIAL_MEDIA_PLATFORMS:
    try: 
        shutil.make_archive(
            base_name=f"./app/aws/lambda/{platform}", 
            format="zip", 
            root_dir=f"./app/scraper/{platform}", 
            base_dir="testLambda.py" ##### CHANGE THIS TO "daily"
        )
    except Exception as e:
        print(e)
    break

# Create lambda functions for all platforms
for platform in SOCIAL_MEDIA_PLATFORMS:
    try:
        with open(f"./app/aws/lambda/{platform}.zip", "rb") as f:
            scraper_code = f.read()

        response = lambda_client.create_function(
            FunctionName=f"{platform}_scheduler",
            Runtime="python3.9",
            Role=role["Role"]["Arn"],
            Handler="testLambda.lambda_handler",
            Code=dict(ZipFile=scraper_code),
            Timeout=300,  # Maximum allowable timeout
        )
    except Exception as e:
        print(e)
    break

# Reinitialize clients
iam_client, lambda_client, s3_resource, role = create_clients()

# Add permission (trigger) and initiate bucket notification for all platforms
for platform in SOCIAL_MEDIA_PLATFORMS:
    try:
        function_name = f"{platform}_scheduler"
        response1 = lambda_client.add_permission(
            StatementId=f"S3_invoke_{function_name}",
            FunctionName=function_name,
            Action="lambda:InvokeFunction",
            Principal="s3.amazonaws.com",
            SourceArn=f"arn:aws:s3:::smt483tls-{platform}-bucket",
            SourceAccount='951045442503'
        )

        bucket_notification = s3_resource.BucketNotification(f"smt483tls-{platform}-bucket")

        response2 = bucket_notification.put(
            Bucket=f"smt483tls-{platform}-bucket",
            NotificationConfiguration={
                "LambdaFunctionConfigurations": [
                    {
                        "LambdaFunctionArn": f"arn:aws:lambda:ap-southeast-1:951045442503:function:{function_name}",
                        "Events": ["s3:ObjectCreated:*"],
                    }
                ]
            }
        )
    except Exception as e:
        print(e)
    break
    

