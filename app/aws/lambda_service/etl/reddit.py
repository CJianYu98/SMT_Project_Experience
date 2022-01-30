import json
from decimal import Decimal

import boto3

REDDIT = [
    'author_fullname', 
    'title', 
    'link_flair_text', 
    'downs', 
    'ups', 
    'upvote_ratio', 
    'score', 
    'is_original_content', 
    'created', 
    'top_awarded_type', 
    'id', 
    'permalink', 
    'num_comments', 
    'media_embed', 
    'thumbnail', 
    'view_count', 
    'over_18', 
    'preview', 
    'author', 
    'all_awardings', 
    'discussion_type', 
    'created_utc', 
    'body_html',
    'comments'
]

REDDIT_COMMENT = [
    'comment_type',
    'total_awards_received',
    'likes',
    'author',
    'created_utc',
    '_submission',
    'score',
    'body',
    'downs',
    'top_awarded_type',
    'permalink',
    'ups',
    'score_hidden',
    'depth',
    'parent_id',
    'id'
]

# Define dynamodb resource
dynamodb = boto3.resource('dynamodb')

def put_dynamodb_row(data: dict, table_name: str) -> None:
    """
    Writes single row data into dynamodb.

    Args:
        data (dict): The input dictionary generated after extracting row data from json
        table_name (str): Name of the dynamodb table
    """

    # Parse floats (not compatible with dynamodb) into decimal
    data = json.loads(json.dumps(data), parse_float=Decimal)
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        batch.put_item(Item=data)

def lambda_handler(event, context):
    """
    Takes in aws event when new raw json file is added to reddit S3 bucket. 
    Goes through every post in the json file and processes it into DynamoDB.
    Variables for each post is first extracted into post_dict.
    Comments for each post are handled seperately and added into comment_dict.

    Args:
        event ([type]): AWS Lambda event arg
        context ([type]): AWS Lambda context arg
    """
    filename = event['Records'][0]['s3']['object']['key']
    s3_resource = boto3.resource("s3", region_name="ap-southeast-1")
    s3_object = s3_resource.Object("smt483tls-reddit-bucket", filename)
    x = s3_object.get()['Body'].read().decode('utf-8')
    data = json.loads(x)

    # Iterate through each post in raw json and begin extracting
    for post_id in data:
        post_dict = {
            variable: data[post_id].get(variable)
            for variable in REDDIT
            if variable != 'comments'
        }

        comments = data[post_id]['comments']
        if comments:
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
