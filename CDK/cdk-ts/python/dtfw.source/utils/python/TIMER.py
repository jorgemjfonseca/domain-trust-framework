# 📚 TIMER

import datetime

def test():
    return 'this is a TIMER test.'


class TIMER:

    timerStart = datetime.datetime.now()

    def Elapsed(self):
        global timerStart
        current = datetime.datetime.now()
        elapsed = (current - timerStart)
        timerStart = current
        output = round(elapsed.total_seconds() * 1000)
        return f'''--> Elapsed: {output} ms
    .
    '''

    def PrintElapsed(self):
        print(f"--- {self.Elapsed()} milliseconds elapsed")

       
    def StartWatch(self):
        return datetime.datetime.now()


    def StopWatch(self, start):
        current = datetime.datetime.now()
        elapsed = (current - start)
        output = round(elapsed.total_seconds() * 1000)
        return f'{output} ms'


    