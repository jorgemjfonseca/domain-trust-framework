# 📚 Subscriber-Updated

# 👉 https://quip.com/9ab7AO56kkxY#temp:C:ISdeb655f34cef549fbbb9669e4a

from time import time
from DYNAMO import DYNAMO
from MSG import MSG
from UTILS import UTILS

table = DYNAMO('DEDUPS')

def handler(event, context):
    print(f'{event}')
    
    msg = MSG(event)
    body = msg.Body()

    id = body['UpdateID']

    item = UTILS.Merge(
        body,
        {
            "Publisher": msg.From(),
            "TTL": int(time()) + (1 * 24 * 60 * 60)
        }
    ) 

    table.Upsert(id, item)

'''
"Body": {
    "UpdateID": "8e8cb55b-55a8-49a5-9f80-439138e340a2",
    "Domain": "example.com",
    "Timestamp": "2018-12-10T13:45:00.000Z"
}
'''