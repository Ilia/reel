import json
import requests
import boto3
import os
import logging

dynamodb = boto3.client('dynamodb')
logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    id = getId(event)
    
    data = fetchDataFromApi(id)
    
    if(str(data['id']) != str(id)):
        return response(code=403, body='Bad Request')

    upsert(id, formatData(data))
    
    return response(body=json.dumps(data))


def getId(event):
    id = None

    if 'reel_id' in event:
        id = event['reel_id']

    if 'Records' in event:
        try:
            id = event.get('Records')[0].get('Sns').get('Message')
        except KeyError as e:
            raise ValueError('Invalid SNS message.')

    if id is None:
        raise ValueError('Invalid Reel ID.')

    return id

def formatData(data):
    # TODO: format data, we dont need to store everything in the cache, just what we need 
    return data

def upsert(id, data): 
    table_name = os.environ.get('CACHE_TABLE', 'ReelCache')
    region = os.environ.get('REGION', 'ap-southeast-2')
    params = {
        'reel_id': {'S': str(id)},
        'data': {'S': json.dumps(data)},
    }
    try:
        return dynamodb.put_item(
            TableName=table_name,
            Item=params
        )
    except (ClientError, ParamValidationError) as e:
        logging.error(e)
        raise
    
def fetchDataFromApi(id):
    api_endpoint = os.environ.get('API_ENDPOINT')
    api_token = os.environ.get('API_TOKEN')

    request = requests.get(api_endpoint + str(id), params={'access_token':api_token})
    json_data = request.json()
    return json_data['response']

def response(code=200, headers={"content-type":"application/json"}, body='Ok'):
    return {
        'statusCode': code,
        'headers' : headers,
        'body': body
    }    