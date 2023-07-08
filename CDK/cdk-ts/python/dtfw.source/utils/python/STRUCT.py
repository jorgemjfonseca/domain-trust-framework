# 📚 STRUCT

# 👉 https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations

# 👉 https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
from typing import List, Set, Tuple, Dict


class RequiredAttributeMissing(Exception):
    pass
class RequiredItemMissing(Exception):
    pass
class AttributeDoesntMatch(Exception):
    pass



class STRUCT: 
    ''' 
    👉 Generic structure that wraps a non-STRUCT object. 
    If a STRUCT object is received to be wrapped, 
    it first unwraps to get the and store only the given inner object.
    '''


    def __init__(self, obj:any, attRoot=None):
        safe = STRUCT.Unstruct(obj)
        self._obj = safe
        self._attRoot = safe 
        if attRoot:
            self._attRoot = attRoot


    @staticmethod
    def Unstruct(obj:any) -> any:
        ''' 👉 If the object is a STRUCT, returns the inner object. '''
        if isinstance(obj, STRUCT):
            return obj.Obj()
        return obj


    def Obj(self):
        ''' 👉 Returns the inner object. '''
        return self._obj


    def __str__(self):
        ''' 👉 Returns the inner object to be used in print(f'{my_struct}'). '''
        return self._obj


    def Print(self, title=None):
        ''' 👉 Prints the json representation of the inner object. '''
        print(f'{title}={self.Obj()}')
    

    def SetAttRoot(self, attRoot:any):
        ''' 
        👉 Sets the root for the Att() method. 
        Useful for an envelope where the attributes are in the body.
        ''' 
        self._attRoot = attRoot 


    def Att(self, name:str, default=None, root=None, set:any=None) -> any:
        """ 
        👉 Sets or gets the value from the referenced attribute. 

        To get chained atributes, use '.' for the hierarchy.

        GIVEN name='Parent' 
         THEN returns self._obj['Parent']

        GIVEN name='Parent.Child' 
         THEN returns self._obj['Parent']['Child']
        """

        # hierarchy navigation
        if root == None:
            root = self._attRoot

        # setter
        if set != None:
            obj = STRUCT(set).Obj()
            self._attRoot[name] = obj
            return set

        # empty getter
        if root == None:
            return default
        
        # root getter
        if '.' not in name:
            if name not in root:
                return default
            return root[name]
        
        # chained getter
        if '.' in name:
            names = name.split('.')
            parent = self.Att(name=names[0])
            names.pop(0)
            child = '.'.join(names)
            return self.Att(name=child, root=parent)
    

    def RequireBool(self, name:str) -> bool:
        """ 👉 Gets the boolean from the mandatory attribute, or throws an exception if missing/empty/non-bool. """
        val = self.Require(name) 
        if not isinstance(val, bool):
            raise Exception(f'Required attribute {name} should be a boolean.')
        return val


    def RequireStr(self, name:str, set:str=None) -> str:
        val = self.Require(name, set=set)
        if val.strip() == '':
            raise Exception(f'Required string attribute {name} should not be empty.')
        return val
    

    def Require(self, name:str=None, set:any=None) -> any: 
        """ 👉 Gets the value from the mandatory attribute, or throws an exception if missing/empty. """
        if not name:
            if not self._obj:
                raise RequiredItemMissing()    
            return self

        ret = self.Att(name, set=set)
        if not ret:
            raise RequiredAttributeMissing(f'Required attribute missing: {name}')
        return ret
        

    def Match(self, name, value):
        """ 👉 Checks if the referenced property value equals the given value. """
        if self.Att(name) != value:
            raise AttributeDoesntMatch(f'Unexpected value for {name}')
        return self
    

    def RequireStruct(self, name:str, set:any=None) -> STRUCT:
        """ 👉 Sets or gets the structure referenced by the mandatory property. """
        att = self.Require(name, set=set)
        return STRUCT(att)
    

    def Struct(self, name:str=None, set:any=None) -> STRUCT:
        """ 
        👉 Returns the structure referenced by the property.
        Without a name, returns the internal object as a structure. 
        """
        if name:
            att = self.Att(name, set=set)
            return STRUCT(att)
        else:
            return STRUCT(self._obj)
    

    def List(self, name:str) -> List[str]:
        """ 👉 Returns a list of strings referenced by the property. """
        list = self.Att(name)
        if list == None:
            return []
        return list
    

    def Structs(self, name:str) -> List[STRUCT]:
        """ 👉 Returns a list of structures referenced by the property. """
        list = self.Att(name)
        if list == None:
            return []
        ret = []
        for element in list:
            item = STRUCT(element)
            ret.append(item)
        return ret
    

    def Copy(self) -> STRUCT:
        """ 👉 Returns a deep copy of the internal object. """
        from copy import deepcopy
        clone = deepcopy(self.Obj())
        return STRUCT(clone)
    

    def Merge(self, struct:STRUCT):
        """ 👉 Merges another structure into this structure. """
        obj1 = self._obj
        obj2 = struct._obj
        obj1.update(obj2)


    def IsMissingOrEmpty(self, name:str=None):
        """ 
        👉 Indicates if an attribute is missing or empty. 
        If no name is given, it looks at the inner object.
        """
        
        # the root
        if name == None:
            return self._obj == None or self._obj == {}
        
        # the attribute
        val = self.Att(name)
        if val == None or str(val).strip() == '':
            return True
        return False


    def Default(self, name:str, default:str):
        """ 👉 Sets the value of a string attribute, if not set. """
        if self.IsMissingOrEmpty(name):
            self.Att(name, set=default)


    def DefaultTimestamp(self, name):
        """ 👉 Sets the value of an attribute to Timestamp, if not set. """
        from UTILS import UTILS
        self.Default(name, UTILS().Timestamp())


    def DefaultGuid(self, name):
        """ 👉 Sets the value of an attribute to UUID, if not set. """
        from UTILS import UTILS
        self.Default(name, UTILS().UUID())


    def RemoveAtt(self, name=str):
        """ 👉 Removes an attribute. """
        del self._obj[name]


    def Canonicalize(self) -> str:
        # 👉️ https://bobbyhadz.com/blog/python-json-dumps-no-spaces
        from UTILS import UTILS
        return UTILS().Canonicalize(self._obj)
    

    def ToJson(self) -> str:
        ''' 👉 Converts the inner object into a json string.'''
        from UTILS import UTILS
        return UTILS().ToJson(self._obj)
    

    def Includes(self, name:str) -> bool:
        ''' 👉 Indicates if an attribute exists.'''
        return not self.IsMissingOrEmpty()
    

    def Contains(self, name:str) -> bool:
        ''' 👉 Indicates if an attribute exists.'''
        return not self.IsMissingOrEmpty()
    

    def AttExists(self, name:str) -> bool:
        ''' 👉 Indicates if an attribute exists.'''
        return not self.IsMissingOrEmpty()