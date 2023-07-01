import boto3
import os
import json
import uuid
import datetime
from urllib import request, parse



def test():
    return 'this is a test.'


events = boto3.client('events')
class BUS:
        
    # 👉 https://blog.knoldus.com/how-to-create-an-eventbridge-application-in-python/
    # 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html
    # 👉 https://boto3.amazonaws.com/v1/documentation/api/1.10.46/reference/services/events.html
    @staticmethod
    def Publish(eventBusName, source, detailType, detail):
        return events.put_events(
            Entries=[
                {
                    'Source':source,
                    'DetailType':detailType,
                    'Detail':detail,
                    'EventBusName':eventBusName
                }
            ]
    )


class MESSENGER:
    
    @staticmethod
    def Send(envelope, source, action):
        # Set or change the subject accordingly.
        MSG(envelope).Subject(action)
        # Add to the bus.
        BUS.Publish(
            eventBusName= 'Messenger-Bus', 
            source= source,
            detailType= 'Messenger-Sender', 
            detail= envelope)


class UTILS: 

    # 👉️ https://stackoverflow.com/questions/37049289/how-do-i-convert-a-python-uuid-into-a-string
    @staticmethod
    def Correlation():
        correlation = str(uuid.uuid4());
        print(f'{correlation=}')
        return correlation


    # 👉️ https://stackoverflow.com/questions/53676600/string-formatting-of-utcnow
    @staticmethod
    def Timestamp():
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        return timestamp


    # 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
    @staticmethod
    def Canonicalize(object: any) -> str:
        canonicalized = json.dumps(object, separators=(',', ':'))
        print(f'{canonicalized=}')
        return canonicalized
    

    # 👉️ https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib    
    @staticmethod
    def Post(url: str, body: any) -> any:
        print(f'{url=}')
        print(f'body={json.dumps(body)}')

        # data = parse.urlencode(body).encode()
        # print(f'{data=}')
        data = bytes(json.dumps(body), encoding='utf-8')
        
        req = request.Request(url=url, method='POST', data=data)
        req.add_header('Content-Type', 'application/json')
        resp = request.urlopen(req)
        
        charset=resp.info().get_content_charset()
        if charset == None:
            charset = 'utf-8'
        content=resp.read().decode(charset)
        
        print(f'{content=}')
        return content


class MSG:
    
    def __init__(self, event):
        self.envelope = event

    def Envelope(self):
        return self.envelope

    def Subject(self, subject=None):
        if subject:
            self.envelope['Header']['Subject'] = subject
        return self.envelope['Header']['Subject']

    def From(self):
        return self.envelope['Header']['From']
    
    def Body(self):
        if 'Body' in self.envelope:
            return self.envelope['Body']
        return {}
    
    @staticmethod
    def Wrap(to, body):
        envelope =  {
            'Header': {
                'To': to
            },
            'Body': body
        }
        msg = MSG(envelope)
        msg.Stamp()
        return msg


    def Stamp(self):
        defaults = {
            'Header': {
                'Correlation': UTILS.Correlation(),
                'Timestamp': UTILS.Timestamp()
            },
            'Body': {}
        }
        print(f'{defaults=}')

        # 👉️ https://stackoverflow.com/questions/14839528/merge-two-objects-in-python
        original = self.envelope
        stamped = defaults
        stamped['Header'].update(original['Header']) 
        if 'Body' in original:
            stamped['Body'].update(original['Body']) 

        self.envelope = stamped
        return stamped


sqs = boto3.client("sqs")
class SQS:
    

    def __init__(self, alias):
        name = os.environ[alias]
        self.url = sqs.get_queue_url(QueueName= name)
        

    def Send(self, msg):
        resp = sqs.send_message(
            QueueName= self.url,
            MessageBody= json.dumps(msg)
        )
        code = resp['ResponseMetadata']['HTTPStatusCode']
        if code != 200:
            raise Exception('Error sending to the queue.')
        return resp
    


lambdaClient = boto3.client('lambda')
class LAMBDA:

    def __init__(self, alias):
        self.name = os.environ[alias]


    # 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/invoke.html
    def invoke(self, params):
        print(f'invoking [{self.name}]({params})...')
        
        response = lambdaClient.invoke(
            FunctionName = self.name,
            Payload=json.dumps(params),
            LogType='Tail')
        
        returned = json.loads(response['Payload'].read())
        print(f'{returned=}')
        return returned



dynamo = boto3.resource('dynamodb')
class DYNAMO:
    
    def __init__(self, alias):
        self.table = DYNAMO._getTable(alias)

    def Upsert(self, id, item):
        item['ID'] = id
        return DYNAMO._update_item(table=self.table, key='ID', body=item)
    
    def Get(self, id):
        return DYNAMO._getItem(self.table, id)
    
    def Delete(self, id):
        return DYNAMO._delete_item(self.table, 'ID', id)
    
    def GetAll(self):
        return DYNAMO._get_items(self)


    @staticmethod
    def _getTable(alias):
        table = dynamo.Table(os.environ[alias])
        return table



    # 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
    @staticmethod
    def _getItem(table, id):
        print (f'{id=}')

        response = table.get_item(
            Key = { 'ID': id }
        )
        print (f'getItem: {response=}')
        
        if 'Item' not in response:
            return None

        item = response['Item']
        print (f'{item=}')
        return item


    @staticmethod
    def _get_update_params(k, body):
        """Given a dictionary we generate an update expression and a dict of values
        to update a dynamodb table.

        Params:
            body (dict): Parameters to use for formatting.

        Returns:
            update expression, dict of values.
        """
        update_expression = ["set "]
        update_values = dict()
        update_names = dict()

        for key, val in body.items():
            if key != k:
                update_expression.append(f" #{key} = :{key},")
                update_values[f":{key}"] = val
                update_names[f"#{key}"] = f"{key}"

        return "".join(update_expression)[:-1], update_values, update_names
            
            
    @staticmethod            
    def _update_item(table, key, body):
        a, v, n = DYNAMO._get_update_params(key, body)
        response = table.update_item(
            Key= {key: body[key]},
            UpdateExpression=a,
            ExpressionAttributeValues=dict(v),
            ExpressionAttributeNames=dict(n)
            )
        return response


    @staticmethod
    def _delete_item(table, key, id):
        response = table.delete_item(Key={ key: id })
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        print(status_code)
        return status_code
        

    @staticmethod
    def my_scan(table, index, start):
        if index != '':
            if start != '':
                print ('my_scan(index="', index, '",start="', start, '")')
                return table.scan(IndexName=index, ExclusiveStartKey=start);
            print ('my_scan(index="', index, '")')
            return table.scan(IndexName=index);
        elif start != '':
            print ('my_scan(start="', start, '")')
            return table.scan(ExclusiveStartKey=start);
        print ('my_scan()')
        return table.scan();
        

    @staticmethod
    def _get_items(table, index=''):
        
        response = DYNAMO.my_scan(table, index, '')
        items = response['Items']
        print ('my_scan.Items returned: ', len(response['Items']))
        
        while 'LastEvaluatedKey' in response:
            lastEvaluatedKey = response['LastEvaluatedKey']
            
            response = my_scan(table, index, lastEvaluatedKey)
            print ('my_scanItems returned: ', len(response['Items']))
            items.extend(response['Items'])
            
        print ('get_items.totalItems:', len(items))
        return items


