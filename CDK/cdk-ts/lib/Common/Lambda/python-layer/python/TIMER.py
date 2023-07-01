import datetime

def test():
    return 'this is a TIMER test.'


class TIMER:

    timerStart = datetime.datetime.now()

    @staticmethod
    def Elapsed():
        global timerStart
        current = datetime.datetime.now()
        elapsed = (current - timerStart)
        timerStart = current
        output = round(elapsed.total_seconds() * 1000)
        return f'''--> Elapsed: {output} ms
    .
    '''

    @staticmethod
    def PrintElapsed():
        print(f"--- {TIMER.Elapsed()} milliseconds elapsed")

       
    @staticmethod
    def StartWatch():
        return datetime.datetime.now()

    @staticmethod
    def StopWatch(start):
        current = datetime.datetime.now()
        elapsed = (current - start)
        output = round(elapsed.total_seconds() * 1000)
        return f'{output} ms'


    