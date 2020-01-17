
import json


def hello(event, context):
    input = json.loads(event['data'])
    print("Input data:", json.dumps(input))
    
    return event['data']
