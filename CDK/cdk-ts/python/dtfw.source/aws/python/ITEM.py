# 📚 ITEM

from STRUCT import STRUCT
from DYNAMO import DYNAMO


class ITEM(STRUCT): 
    ''' 👉 STRUCT created from a DynamoDB item. '''

    def __init__(self, item:any, table:DYNAMO=None):
        if table != None:
            self._table = table
        elif isinstance(item, ITEM):
            self._table = item._table

        if not self._table:
            raise Exception('Table is required!')

        super().__init__(item)


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


    def Save(self):
        ''' 👉 Updates the item on its original table. '''       
        self.Table().Update(self)