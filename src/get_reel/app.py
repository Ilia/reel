import json
import urllib3
import boto3

from common import response 

dynamodb = boto3.client('dynamodb')
lam = boto3.client('lambda')

def lambda_handler(event, context):
    
    # TODO: need to ensure event query parameter is available and valid 
    id = event['queryStringParameters']['id']
    item = getReel(id).get('Item')

    if not item:
        # TODO: cache the reel and response in real time - is there a better way?
        return response(body={})

    return response(body=item.get('data').get('S'))    
        

def getReel(id):
    table_name = os.environ.get('CACHE_TABLE', 'reels')
    region = os.environ.get('REGION', 'ap-southeast-2')
    params = {
        'id': {'S': str(id) }
    }

    return dynamodb.get_item(
        TableName=table_name, 
        Key=params
    )
    
def cacheReel(id):
    # TODO: cache the reel
    payload = {}
    payload['reel_id'] = id
        
    response = lam.invoke(
        FunctionName='cacheReel',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload))
    response_payload = json.loads(response['Payload'].read().decode("utf-8"))            
    return response_payload['body']