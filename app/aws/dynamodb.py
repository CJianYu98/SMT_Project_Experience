import boto3

from .constant import SOCIAL_MEDIA_PLATFORMS


def dynamodb_setup():
    """
    
    """
    
    dynamodb = boto3.client("dynamodb")  # Establish dynamodb client

    try:
        for platform in SOCIAL_MEDIA_PLATFORMS:
            response = dynamodb.create_table(
                TableName=f'{platform}-table',
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "created_datetime", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},
                    {"AttributeName": "created_datetime", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 100, "WriteCapacityUnits": 100},
            )
            print(response)
            break

            # if response['HTTPStatusCode'] > 299:
            #     raise Exception
            
    except Exception as e:
        print(e)

dynamodb_setup()