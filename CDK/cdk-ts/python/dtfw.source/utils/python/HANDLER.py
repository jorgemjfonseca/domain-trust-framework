# 📚 HANDLER


from AWS import AWS
from UTILS import UTILS


class HANDLER(AWS, UTILS): 
    ''' 🏃 Registers and triggers code events. '''


    def __init__(self):
        self.Memory = []
        if self.Enrironment('TRIGGERS'):
            self.Table = self.Dynamo('TRIGGERS', keys=['Event'])


    def On(self, event:str, trigger:object):
        ''' 
        🏃 Registers a trigger for the event \n
        👉 https://stackoverflow.com/questions/307494/function-pointers-in-python \n
        👉 https://d-hanshew.medium.com/cleaner-code-using-function-pointers-in-python-75c49f04b6f2 '''
        if event not in self.Memory:
            self.Memory[event] = []
        self.Memory[event].append(trigger)


    def Trigger(self, event, *args):
        ''' 
        🏃 Runs all triggers registered for the event. \n
        👉 https://stackoverflow.com/questions/13783211/how-to-pass-an-argument-to-a-function-pointer-parameter 
        '''

        # Read from memory
        if event in self.Memory:
            event = self.Memory[event]
            for trigger in event:
                trigger(*args)

        # Read from Dynamo
        if self.Table:
            ret = None
            event = self.Table.Get({ 'Event': event })
            for trigger in event.Structs('Triggers'):
                name = trigger.Att('Lambda')
                if name: 
                    ret = self.Lambda(name).Invoke(*args)
            # return the value of the last invocation.
            return ret
