import json
from os import fsdecode

from . import config
# from src.config import * # VAR directly can be called

# import config
# from config import *  --  "name 'config' is not defined"
# import config -- module 'config' has no attribute 'VAR1'"


def hello(event, context):
    msg = "Go Serverless v1.0! Your function executed successfully! "+str(config.VAR1)
    body = {
        "message": msg,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
# print(hello(
#         {"key1": "value1"},
#         {"key2": "value2"},
#     ),)
print(hello({"key3": "value3"},{"key2": "value2"}),)