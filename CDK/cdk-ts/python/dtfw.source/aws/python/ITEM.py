# 📚 ITEM

from STRUCT import STRUCT
from DYNAMO import DYNAMO


class ITEM(STRUCT): 
    ''' 👉 STRUCT created from a DynamoDB item. '''

    def __init__(self, item:any, table:DYNAMO):
        if not item:
            raise Exception('Item is required!')
        if not table:
            raise Exception('Table is required!')
        
        super().__init__(item)
        self._table = table


    def ID(self) -> str:
        ''' 👉 The ID property. '''
        return self.Require('ID')


    def Table(self):
        if not self._table:
            raise Exception('Table not defined!')
        return self._table
    

    def Delete(self):
        ''' 👉 Deletes the item from its original table. '''
        self.Table().Delete(self)


    def Update(self):
        ''' 👉 Updates the item on its original table. '''       
        self.Table().Update(self)