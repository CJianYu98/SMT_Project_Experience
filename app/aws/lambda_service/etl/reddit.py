import json
import pprint
from decimal import Decimal
from logging import exception

import boto3

from ...constant import REDDIT, REDDIT_COMMENT

# Define dynamodb resource
dynamodb = boto3.resource('dynamodb')

def put_dynamodb_row(data: dict, table_name: str) -> None:
    """
    Writes single row data into dynamodb

    Args:
        data (dict): The input dictionary generated after extracting row data from json
        table_name (str): Name of the dynamodb table
    """

    # Parse floats (not compatible with dynamodb) into decimal
    data = json.loads(json.dumps(data), parse_float=Decimal)
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        batch.put_item(Item=data)

# f = open('./app/aws/lambda/etl/2022-01-28.json')
# data = json.load(f)


def lambda_handler(event, context):

    filename = event['Records'][0]['s3']['object']['key']
    s3_resource = boto3.resource("s3", region_name="ap-southeast-1")
    s3_object = s3_resource.Object("smt483tls-reddit-bucket", filename)
    x = s3_object.get()['Body'].read().decode('utf-8')
    data = json.loads(x)

    # Iterate through each post in raw json and begin extracting
    for post_id in data:
        post_dict = {}

        #Iterate through every variable in a post
        for variable in REDDIT:
            # If variable is not 'comments', add it to post_dict
            if variable != 'comments':
                post_dict[variable] = data[post_id].get(variable)
            # If variable is 'comments'
            else:
                comments = data[post_id][variable]
                if comments:
                    # Loop through every comment id and put to dynamodb
                    for cid in comments:
                        comment_dict = {
                            comment_variable: comments[cid].get(comment_variable)
                            for comment_variable in REDDIT_COMMENT
                        }
                        # Change dictionary key name to be consistent with dynamodb table
                        comment_dict['post_id'] = comment_dict.pop('_submission')
                        put_dynamodb_row(comment_dict, 'reddit-comment-table')

        # Put post to dynamodb
        put_dynamodb_row(post_dict, 'reddit-post-table')
        print(f'post {post_id} done')
