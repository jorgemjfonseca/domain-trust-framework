# 📚 HANDLER


from AWS import AWS
from UTILS import UTILS


# ✅ DONE
class HANDLER(AWS, UTILS): 
    ''' 🏃 Registers and triggers code events. '''


    def __init__(self):
        self.Memory = []
        self.Table = self.DYNAMO('HANDLERS')


    # ✅ DONE
    def On(self, event:str, trigger:object):
        ''' 
        🏃 Registers a trigger for the event \n
        👉 https://stackoverflow.com/questions/307494/function-pointers-in-python \n
        👉 https://d-hanshew.medium.com/cleaner-code-using-function-pointers-in-python-75c49f04b6f2 '''
        if event not in self.Memory:
            self.Memory[event] = []
        self.Memory[event].append(trigger)


    # ✅ DONE
    def Trigger(self, event, *args):
        ''' 
        🏃 Runs all triggers registered for the event. \n
        👉 https://stackoverflow.com/questions/13783211/how-to-pass-an-argument-to-a-function-pointer-parameter 
        '''

        # Read from memory and execute the python functin.
        if event in self.Memory:
            event = self.Memory[event]
            for trigger in event:
                trigger(*args)

        # Read from Dynamo and invoke the lambda function.
        if self.Table:
            ret = None
            event = self.Table.Get(event)
            for trigger in event.List('Lambdas'):
                ret = self.LAMBDA(trigger).Invoke(*args)
            # return the value of the last invocation.
            return ret
