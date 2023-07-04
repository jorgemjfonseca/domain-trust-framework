# 📚 DYNAMO

import boto3
import os
from time import time

from DTFW import DTFW
dtfw = DTFW()


def test():
    return 'this is a DYNAMO test.'


dynamo = boto3.resource('dynamodb')
class DYNAMO:
    

    def __init__(self, alias=None):
        if alias:
            self._table = self._getTable(alias)


    def Merge(self, id, item):
        item['ID'] = id
        return self._update_item(table=self._table, key='ID', body=item)
    

    def Get(self, id):
        if not id:
            return None
        return self._getItem(self._table, id)
    

    def Item(self, id):
        return dtfw.Item(self.Get(id))
    

    def Delete(self, id):
        return self._delete_item(self._table, 'ID', id)
    
    
    def GetAll(self):
        return self._get_items(self)


    def _getTable(self, alias):
        table = dynamo.Table(os.environ[alias])
        return table



    # 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
    def _getItem(self, table, id):
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


    def _get_update_params(self, k, body):
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
            
                  
    def _update_item(self, table, key, body):
        a, v, n = self._get_update_params(key, body)
        response = table.update_item(
            Key= {key: body[key]},
            UpdateExpression=a,
            ExpressionAttributeValues=dict(v),
            ExpressionAttributeNames=dict(n)
            )
        return response


    def _delete_item(self, table, key, id):
        response = table.delete_item(Key={ key: id })
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        print(status_code)
        return status_code
        

    def my_scan(self, table, index, start):
        if index != '':
            
            if start != '':
                print ('my_scan(index="', index, '",start="', start, '")')
                return table.scan(IndexName=index, ExclusiveStartKey=start)
            
            print ('my_scan(index="', index, '")')
            return table.scan(IndexName=index)
        
        elif start != '':
            print ('my_scan(start="', start, '")')
            return table.scan(ExclusiveStartKey=start)
        
        print ('my_scan()')
        return table.scan()
        

    def _get_items(self, table, index=''):
        
        response = self.my_scan(table, index, '')
        items = response['Items']
        print ('my_scan.Items returned: ', len(response['Items']))
        
        while 'LastEvaluatedKey' in response:
            lastEvaluatedKey = response['LastEvaluatedKey']
            
            response = self.my_scan(table, index, lastEvaluatedKey)
            print ('my_scanItems returned: ', len(response['Items']))
            items.extend(response['Items'])
            
        print ('get_items.totalItems:', len(items))
        return items


    def TTL(self, days):
        return int(time()) + (days * 24 * 60 * 60)
    

    def GetPageFromTimestamp(self, timestamp, exclusiveStartKey = {}):
        ''' 
        👉 https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html 
        👉 https://stackoverflow.com/questions/49344272/finding-items-between-2-dates-using-boto3-and-dynamodb-scan
        '''

        filter = {
            #'TableName': TABLE_NAME,
            #'IndexName': "main-index",
            'Select': "ALL_ATTRIBUTES",
            #'ExclusiveStartKey': exclusiveStartKey,
            'ExpressionAttributeNames': {
                "#f_up": "Timestamp"
            },
            'ExpressionAttributeValues': {
                ":s_time": timestamp,
                ":e_time": dtfw.Utils().Timestamp()
            },
            'FilterExpression': "#f_up between :s_time and :e_time",
            'ScanIndexForward': "true"
        }

        if exclusiveStartKey:
            response = self._table.scan(
                FilterExpression=filter, 
                ExclusiveStartKey=exclusiveStartKey)
        else:
            response = self._table.scan(
                FilterExpression=filter)
        
        return response
        '''
        {
            'Items': [...],
            'LastEvaluatedKey': {...}
        }
        '''


    def Records(self, event):
        ''' 
        👉 https://stackoverflow.com/questions/63126782/how-to-desalinize-json-coming-from-dynamodb-stream 
        👉 https://stackoverflow.com/questions/63050735/how-to-design-dynamodb-to-elastic-search-with-insert-modify-remove
        👉 https://www.thelambdablog.com/getting-dynamodb-data-changes-with-streams-and-processing-them-with-lambdas-using-python/
        👉 https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.Tutorial.html
        '''

        if 'Records' not in event:
            return event
        
        result = []
        for r in event['Records']:
            tmp = {}

            for k, v in r['dynamodb']['NewImage'].items():
                if "S" in v.keys() or "BOOL" in v.keys():
                    tmp[k] = v.get('S', v.get('BOOL', False))
                elif 'NULL' in v:
                    tmp[k] = None

            result.append(tmp)

        return result