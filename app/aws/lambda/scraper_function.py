import boto3
import json

client = boto3.client('events')
lambda_client = boto3.client('lambda')

rule = client.put_rule(
    Name="Rate1Min",
    ScheduleExpression="rate(1 minute)",
    State="ENABLED",
    RoleArn="arn:aws:iam::951045442503:role/LambdaTestingRole1"
)

client.put_targets(
    Rule="Rate1Min",
    Targets=[
        {
            "Id": "TestingRuleId",
            "Arn": "arn:aws:lambda:ap-southeast-1:951045442503:function:schedulerLambda",
            # "Input": json.dumps({"foo": "bar"})
        }
    ]
)

lambda_client.add_permission(
    FunctionName="arn:aws:lambda:ap-southeast-1:951045442503:function:schedulerLambda",
    StatementId="TestingRule",
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn="arn:aws:events:ap-southeast-1:951045442503:rule/Rate1Min"
)