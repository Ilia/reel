import json
import requests
import boto3
import os

from common import response 
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO: ensure we have proper validation
    id = event['Records'][0]['Sns']['Message']
    data = fetchDataFromApi(id)
    
    if(str(data['id']) != str(id)):
        return response(code=403, body='Bad Request')

    upsert(id, formatData(data))
    
    return response(body=json.dumps(data))


def formatData(data):
    # TODO: format data, we dont need to store everything in the cache, just what we need 
    return data

def upsert(id, data): 
    table_name = os.environ.get('CACHE_TABLE', 'reels')
    region = os.environ.get('REGION', 'ap-southeast-2')
    params = {
        'reel_id': {'S': str(id)},
        'data': {'S': json.dumps(data)},
    }
    return dynamodb.put_item(
        TableName=table_name,
        Item=params
    )
    
def fetchDataFromApi(id):
    api_endpoint = os.environ.get('API_ENDPOINT')
    api_token = os.environ.get('API_TOKEN')

    request = requests.get(api_endpoint + str(id), params={'access_token':api_token})
    json_data = request.json()
    return json_data['response']
    