import json
import boto3


def lambda_handler(event, context):
    filename = event['Records'][0]['s3']['object']['key']

    s3_resource = boto3.resource("s3", region_name="ap-southeast-1")
    s3_object = s3_resource.Object("smt483tls-twitter-bucket", filename)

    x = s3_object.get()['Body'].read().decode('utf-8')
    y = json.loads(x)
    print(y['hello'])

    return {
        'statusCode': 200,
        'body': 'Hello World'
    }



#### Testing code for adding data to table
s3_resource = boto3.resource("s3", region_name="ap-southeast-1")
s3_object = s3_resource.Object("smt483tls-twitter-bucket", 'submissions_copy.json')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('reddit-table')

x = s3_object.get()['Body'].read().decode('utf-8')
y = json.loads(x)
y['id'] = "1"
y['created_datetime'] = '20220101'
print(y)

temp = []
temp.append(y)
for i in range(2, 7):
    z = {
        "id": str(i),
        "created_datetime": f'2020-{i}',
        "col1": f'data-{1}'
    }
    temp.append(z)
# response = table.put_item(
#     Item = y
# )




print(batch)

