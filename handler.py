import json
import boto3
import os
from datetime import datetime
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name=str(os.environ['REGION_NAME']))
dbtable = str(os.environ['DYNAMODB_TABLE'])

def blogPosts(event, context):
    table = dynamodb.Table(dbtable)
    myPost_str = event['body']
    myPost = json.loads(myPost_str)

    bucket = myPost['bucket']['name']
    key = myPost['bucket']['key']
    imageUrl = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    response = table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'imageUrl': str(imageUrl),
            'category': myPost['category'],
            'title': myPost['title'],
            'paragraph': myPost['paragraph'],
            'blogUrl': myPost['blogUrl'],
            'createdAt': str(datetime.now()) 
        }
    )
    return {
        "headers": { "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" },
        "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
        "body": "Post has been successfully added!",
    }

def blogList(event, context):
    table = dynamodb.Table(dbtable)
    response = table.scan()

    return {
        "headers": { "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" },
        "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
        "body": json.dumps(response['Items']),
        "isBase64Encoded": False,
    }


def getPost(event, context):
    table = dynamodb.Table(dbtable)
    response = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    if 'Item' in response:
        return {
            "headers": { "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*" },
            "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
            "body": json.dumps(response['Item']),
            "isBase64Encoded": False,
        }
    else:
        return {
            "statusCode": 404,
            "body": "Post not found.",
        }


def deletePost(event, context):
    table = dynamodb.Table(dbtable)
    post_id = event['pathParameters']['id']

    response = table.delete_item(
        Key={
            'id': post_id
        }
    )

    return {
        "headers": { "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*" },
        "statusCode": response['ResponseMetadata']['HTTPStatusCode'],
        "body": "Post has been successfully deleted!",
        "isBase64Encoded": False,
    }
