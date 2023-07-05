# 📚 BROKER

def test():
    return 'this is BROKER test.'


from DTFW import DTFW
dtfw = DTFW()


class BROKER:
    ''' 👉 https://quip.com/SJadAQ8syGP0/-Broker '''

    
    def Binds(self):
        ''' 👉 https://quip.com/oSzpA7HRICjq/-Broker-Binds '''
        if not self._binds:
            from BROKER_BINDS import BROKER_BINDS
            self._binds = BROKER_BINDS()
        return self._binds

    
    def Credentials(self):
        ''' 👉 https://quip.com/sN8DACFLN9wM#AfTABAujlEx '''
        if not self._credentials:
            from BROKER_CREDENTIALS import BROKER_CREDENTIALS
            self._credentials = BROKER_CREDENTIALS()
        return self._credentials


    def Pay(self):
        ''' 👉 https://quip.com/NBngAvaOflZ6#FIJABArj7az '''
        if not self._pay:
            from BROKER_PAY import BROKER_PAY
            self._pay = BROKER_PAY()
        return self._pay


    def Prompt(self):
        ''' 👉 https://quip.com/FNbzAVSVu9z6#RCPABAYylHR '''
        if not self._prompt:
            from BROKER_PROMPT import BROKER_PROMPT
            self._prompt = BROKER_PROMPT()
        return self._prompt


    def Sessions(self):
        ''' 👉 https://quip.com/HrgkAuQCqBez#bXDABAe5brB '''
        if not self._sessions:
            from BROKER_SESSIONS import BROKER_SESSIONS
            self._sessions = BROKER_SESSIONS()
        return self._sessions


    def Setup(self):
        ''' 👉 https://quip.com/zaYoA4kibXAP/-Broker-Setup '''
        if not self._setup:
            from BROKER_SETUP import BROKER_SETUP
            self._setup = BROKER_SETUP()
        return self._setup


    def Share(self):
        ''' 👉 https://quip.com/rKzMApUS5QIi#WTIABAsxxkW '''
        if not self._share:
            from BROKER_SHARE import BROKER_SHARE
            self._share = BROKER_SHARE()
        return self._share