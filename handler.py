import json
import logging
import boto3
from botocore.exceptions import ClientError
from uuid import uuid4


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

# def getSignedUrl(bucket_name="project-29-s3-bucket", object_name=uuid4(),
#                           fields=None, conditions=None, expiration=300):
#     s3_client = boto3.client('s3')    
#     try:
#         response = s3_client.generate_presigned_post(bucket_name,
#                                                      object_name,
#                                                      Fields=fields,
#                                                      Conditions=conditions,
#                                                      ExpiresIn=expiration)
#     except ClientError as e:
#         logging.error(e)
#         return None

#     # The response contains the presigned URL and required fields
#     return response


def getSignedUrl(event, context):
    s3_client = boto3.client('s3')  
    try:
        bucket = "project-29-s3-bucket"
        key = str(uuid4()) + ".jpg"
        expireSeconds = 60

        url = s3_client.generate_presigned_url('put_object', 
                                               Params = {'Bucket': bucket, 'Key': key, 'ContentType': 'image/jpg'}, 
                                               ExpiresIn = expireSeconds)

        # url = s3_client.generate_presigned_post(bucket,
        #                                         key,
        #                                         Fields={"Content-Type": "image/jpg"},
        #                                         Conditions=["starts-with", "$Content-Type", "image/"],
        #                                         ExpiresIn=expireSeconds)
        print(url)
        return {"statusCode": 200, 
                "headers":{
                    "Access-Control-Allow-Origin": "*",
                    'Content-Type': 'application/json'
                },
                "body": json.dumps({'url': url})}

    except Exception as e:
        return {"statusCode": 400, 
                "headers":{
                    "Access-Control-Allow-Origin": "*",
                    'Content-Type': 'application/json'
                },
                "body": json.dumps(str(e))}
    
# def executePayload(event, context):
#     s3Event = event