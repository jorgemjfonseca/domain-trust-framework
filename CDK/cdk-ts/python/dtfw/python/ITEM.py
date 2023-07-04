# 📚 ITEM

from ITEM import ITEM


def test():
    return 'this is a ITEM test.'


class RequiredAttributeMissing(Exception):
    pass
class RequiredItemMissing(Exception):
    pass
class AttributeDoesntMatch(Exception):
    pass



class ITEM: 

    def __init__(self, item):
        self._item = item


    def Att(self, name:str, default=None, obj=None) -> any:
        if obj == None:
            obj = self.Item
        if obj == None:
            return default
        
        if '.' not in name:
            if name not in obj:
                return default
            return obj[name]
        
        if '.' in name:
            names = name.split('.')
            parent = self.Att(name=names[0])
            names.pop(0)
            child = '.'.join(names)
            return self.Att(name=child, obj=parent)
    
    
    def Item(self, name:str) -> ITEM:
        return ITEM(self.Att(name))
    

    def Require(self, name: str=None) -> any: 
        if not name:
            if not self._item:
                raise RequiredItemMissing()    
            return self
        else:
            ret = self.Att(name)
            if not ret:
                raise RequiredAttributeMissing(f'Required attribute missing: {name}')
            return ret
        

    def Match(self, name, value):
        if self.Att(name) != value:
            raise AttributeDoesntMatch(f'Unexpected value for {name}')
        return self