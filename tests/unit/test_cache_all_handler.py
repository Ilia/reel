import json
import pytest
import os
import json 
from requests.exceptions import HTTPError, Timeout

from cache_all import app

# @todo: how do I DRY this

@pytest.fixture()
def test_environ():
    """Load environment variables to mock example"""
    # data = {}    
    # with open("test.env.json") as json_file:
    #     data = json.load(json_file)
    # for (k, v) in data["cachelAllFunction"].items():
    #     os.environ[k] = str(v)
    # print (data)
    return data

def test_success(mocker):
    mocker.patch( 'cache_all.app.fetch_reels', return_value={'response':[{"id":1}]} )
    mocker.patch( 'cache_all.app.cache_reel', return_value=[] )

    ret = app.lambda_handler({}, "")
    assert ret["statusCode"] == 200
    assert ret["body"] == 'Ok'

def test_api_failure(mocker):
    mocker.patch( 'cache_all.app.fetch_reels', return_value={'error':{}} )
    mocker.patch( 'cache_all.app.cache_reel', return_value=[] )

    ret = app.lambda_handler({}, "")
    assert ret["statusCode"] == 400
    assert ret["body"] == 'Could not get proper response from Reel API'

def test_api_500_failure(mocker):

    mocker.patch( 'cache_all.app.fetch_reels', side_effect=HTTPError, return_value=[])
    mocker.patch( 'cache_all.app.cache_reel', return_value=[] )
    
    ret = app.lambda_handler({}, "")
    assert ret["statusCode"] == 500
    assert ret["body"] == 'Failed getting response from Reel API'
