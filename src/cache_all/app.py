import json
import requests
import boto3
import os

from common import response 

client = boto3.client('sns') 

def lambda_handler(event, context):
    request = requests.get(os.environ['API_ENDPOINT'], params={'access_token':os.environ['API_TOKEN']})
    json_data = request.json()
    for data in json_data['response']:
        cacheReel(data['id'])
    return response()

def cacheReel(id):   
    client.publish(
        TargetArn=os.environ['CACHE_TOPIC_ARN'],
        Message=json.dumps({'default': json.dumps(id)}),
        MessageStructure='json'
    )
    
    