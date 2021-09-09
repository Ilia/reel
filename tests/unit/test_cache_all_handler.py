import json
import pytest
from pathlib import Path
import os

from cache_all import app


@pytest.fixture()
def test_environ():
    """Load environment variables to mock"""
    # data = {}    
    # with open("test.env.json") as json_file:
    #     data = json.load(json_file)
    # for (k, v) in data["cachelAllFunction"].items():
    #     os.environ[k] = str(v)
    # print (data)
    return data


def test_cache_all_lambda_handler(mocker):
    # todo: work out why fixture is not working
    # todo: we are working with cloud SNS topic, is there any other way? 
    data = {}    
    data_folder = Path("./tests/unit")
    file_to_open = data_folder / "test.env.json"
    print (file_to_open)
    with open(file_to_open) as json_file:
        data = json.load(json_file)
    for (k, v) in data["cachelAllFunction"].items():
        os.environ[k] = str(v)

    print (data)

    ret = app.lambda_handler({}, "")
    
    assert ret["statusCode"] == 200
    assert ret["body"] == 'Ok'