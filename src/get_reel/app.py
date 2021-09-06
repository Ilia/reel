import json
import os
import boto3
from common import response

dynamodb = boto3.client('dynamodb')
lam = boto3.client('lambda')

def lambda_handler(event, context):
    
    if ('pathParameters' not in event 
            or event['httpMethod'] != 'GET'):
        return response(code=400, body=json.dumps({'msg': 'Bad Request'}))

    # TODO: need to ensure event query parameter is available and valid 
    id = event['pathParameters']['id']
    item = getReel(id).get('Item')

    if not item:
        # TODO: this is realtime, is there a better way?
        return response(body=fetchReel(id))

    return response(body=item.get('data').get('S'))    
        

def getReel(id):
    table_name = os.environ.get('CACHE_TABLE', 'ReelCache')
    region = os.environ.get('REGION', 'ap-southeast-2')
    params = {
        'reel_id': {'S': str(id) }
    }

    return dynamodb.get_item(
        TableName=table_name, 
        Key=params
    )
    
def fetchReel(id):
    payload = {
        "reel_id": id
    }
        
    response = lam.invoke(
        FunctionName=os.environ.get('FETCH_FUNCTION'),
        InvocationType='RequestResponse',
        Payload=json.dumps(payload))
    response_payload = json.loads(response['Payload'].read().decode("utf-8"))            
    return response_payload['body']