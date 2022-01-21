import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

my_config = Config(
    region_name = os.getenv("AWS_REGION"),
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# # Get Dynamodb service resource / client
# client = boto3.client("dynamodb")
# db = boto3.resource("dynamodb") # Higher level API

# # Create tables
# __TableName__ = "People"
# Primary_Column_Name = 'Sr'
# Primary_Key = 1
# columns = ["Age", "First", "Last"]

# table = db.Table(__TableName__)


def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            config = my_config,
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            )

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    movie_table = create_movie_table()
    print("Table status:", movie_table.table_status)
