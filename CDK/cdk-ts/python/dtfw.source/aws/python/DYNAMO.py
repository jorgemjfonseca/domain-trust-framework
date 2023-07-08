# 📚 DYNAMO

import boto3
import botocore
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import os
from time import time

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict

from ITEM import ITEM
from STRUCT import STRUCT
from UTILS import UTILS
utils = UTILS()

def test():
    return 'this is a DYNAMO test.'


dynamo = boto3.resource('dynamodb')
class DYNAMO:
    

    def __init__(self, alias=None, keys:List[str]=None):
        if alias:
            self._table = self._getTable(alias)
        self._keys = keys


    def _calculateID(self, struct:STRUCT) -> str:
        ''' 
        👉 Returns the ID from a set of table keys\n
        GIVEN a table with keys==[C,A] 
        WHEN received a struct={A:x, B:y, C:z}
         THEN returns "z/x" 
        '''
        if not self._keys:
            return struct.Require('ID')
        
        vals = []
        for key in self._keys:
            vals.append(struct.Require(key))
        return '/'.join(vals)


    def Get(self, key:any) -> ITEM:
        ''' 
        👉 Gets the item with ID=key, or where the compositive key can be derived from the atributes of the given object.\n
        GIVEN a table with keys=[ID,A,C]
        WHEN received key={A:x, B:y, C:z}       
         THEN return item where ID={x/z}" 

        WHEN received key=123
         THEN return item where ID=123

        WHEN received key='abc'
         THEN return item where ID='abc'
        '''
        if not key:
            return None
        
        id = None
        if isinstance(key, str) or isinstance(key, int):
            id = key
        elif isinstance(key, str):
            id = self._calculateID(key)
        else:
            struct = STRUCT(key)
            id = self._calculateID(struct)

        return ITEM(
            item= self._getItem(self._table, id), 
            table= self)
    

    def GetByID(self, id:str) -> ITEM:
        if not id:
            return None
        return ITEM(self._getItem(self._table, id), table=self)
    

    def Item(self, struct:STRUCT) -> ITEM:
        return self.Get(struct)
    

    def _save(self, any: any, method):  
        struct = STRUCT(any)

        struct.Default('ID', self._calculateID())

        return self._update_item(
            table=self._table, 
            key='ID', 
            body=struct.Obj(),
            method= method)


    def Insert(self, any: any):
        self._save(any=any, method='INSERT')
    

    def Update(self, any: any):
        self._save(any=any, method='UPDATE')        
    

    def Upsert(self, any: any):
        self._save(any=any, method='INSERT,UPDATE')


    def Delete(self, struct: STRUCT):
        id = struct.Require['ID']
        return self._delete_item(self._table, 'ID', id)
    
    
    def GetAll(self):
        return self._get_items(self)


    def _getTable(self, alias):
        name = os.environ[alias]
        if name == None:
            return None
        table = dynamo.Table(name)
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
            
                  
    def _update_item(self, table, key, body, method):
        
        ''' 👉 https://www.tecracer.com/blog/2021/07/implementing-optimistic-locking-in-dynamodb-with-python.html '''
        ''' 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/conditions.html '''
        condition = None
        if 'INSERT' == method:
            condition = Attr('ID').not_exists()
        elif 'UPDATE' == method and 'ItemVersion' in body:
            condition = Attr('RecVersion').eq(body['ItemVersion']) 

        # optimistic concurrency
        body['ItemVersion'] = utils.UUID()

        # get paragmeters
        a, v, n = self._get_update_params(key, body)

        try:
            response = table.update_item(
                Key= {key: body[key]},
                UpdateExpression=a,
                ExpressionAttributeValues=dict(v),
                ExpressionAttributeNames=dict(n),
                # 👉 https://www.tecracer.com/blog/2021/07/implementing-optimistic-locking-in-dynamodb-with-python.html
                ConditionExpression= condition
            )

        except ClientError as err:
            if err.response["Error"]["Code"] == 'ConditionalCheckFailedException':
                # Somebody changed the item in the db while we were changing it!
                raise ValueError("Record changed concurrently, retry!") from err
            else:
                raise err

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
                ":e_time": utils.Timestamp()
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