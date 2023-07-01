def test():
    return 'this is a test.'

# 👉 https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/
def getItem(table, id):
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