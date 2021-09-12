import json
import requests
import boto3
import os
import logging

from common import response

client = boto3.client('sns') 
logger = logging.getLogger('boto3')

def lambda_handler(event, context):
    try:
        json_data = fetch_reels()
        print (json_data)
    except requests.exceptions.RequestException as e: 
        logging.critical(e, exc_info=True) 
        return response(code=500, body="Failed getting response from Reel API")

    if 'response' not in json_data:
        return response(code=400, body="Could not get proper response from Reel API")

    for data in json_data['response']:
        cache_reel(id=int(data['id']))
    
    return response()

def cache_reel(id):   
    return client.publish(
        TargetArn=os.environ['CACHE_TOPIC_ARN'],
        Message=json.dumps({'default': json.dumps(id)}),
        MessageStructure='json'
    )

def fetch_reels():
    request = requests.get(os.environ['API_ENDPOINT'], 
        params={'access_token':os.environ['API_TOKEN']})

    return request.json()