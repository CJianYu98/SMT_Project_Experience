import shutil

import boto3

iam_client = boto3.client("iam")
lambda_client = boto3.client("lambda")
s3 = boto3.client("s3")
s3_resource = boto3.resource('s3')
bucket_notification = s3_resource.BucketNotification('smt483tls-twitter-bucket')

shutil.make_archive("./app/aws/lambda/test", "zip", root_dir="./app/aws/lambda", base_dir="test.py")

with open("./app/aws/lambda/test.zip", "rb") as f:
    zipped_code = f.read()

role = iam_client.get_role(RoleName="LambdaTestingRole1")

response = lambda_client.create_function(
    FunctionName="schedulerLambda1",
    Runtime="python3.9",
    Role=role["Role"]["Arn"],
    Handler="test.lambda_handler",
    Code=dict(ZipFile=zipped_code),
    Timeout=300,  # Maximum allowable timeout
)

response1 = lambda_client.add_permission(
    StatementId="S3InvokeHelloWorldLambda",
    FunctionName="helloWorldLambda",
    Action="lambda:InvokeFunction",
    Principal="s3.amazonaws.com",
    SourceArn="arn:aws:s3:::smt483tls-twitter-bucket",
    SourceAccount='951045442503'
)

response2 = bucket_notification.put(
    Bucket="smt483tls-twitter-bucket",
    NotificationConfiguration={
        "LambdaFunctionConfigurations": [
            {
                "LambdaFunctionArn": "arn:aws:lambda:ap-southeast-1:951045442503:function:helloWorldLambda",
                "Events": ["s3:ObjectCreated:*"],
            }
        ]
    }
)
