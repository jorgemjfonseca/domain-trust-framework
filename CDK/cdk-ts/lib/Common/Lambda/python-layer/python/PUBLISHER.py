
def test():
    return 'this is PUBLISHER test.'


class PUBLISHER:
    

    @staticmethod
    def _HandleFanOuter(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher

        print(f'{event}')

        from MSG import MSG
        msg = MSG(event)
        msg.Subject('Subcriber-Update')

        from MESSENGER import MESSENGER
        MESSENGER.Send(msg, source='Publisher-FanOuter')
    

    @staticmethod
    def _HandlePublisher(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher

        print(f'{event}')

        from MSG import MSG
        body = MSG(event).Body()

        from SQS import SQS
        fanout = SQS('FANOUT')
        
        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')

        for sub in subscribers.GetAll():
            to = sub['Domain']
            msg = MSG().Wrap(to, body)
            fanout.Send(msg)


    @staticmethod
    def _HandleRegister(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        from DYNAMO import DYNAMO
        from MSG import MSG

        subscribers = DYNAMO('SUBSCRIBERS')

        domain = MSG(event).From()
        
        subscribers.Merge(domain, {
            'Domain': domain,
            'Filter': {},
            'Status': 'REGISTERED'
        })


    @staticmethod
    def _HandleReplay(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK1a95aeba490844ce9168b7f4d

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            },
            "Body": {
                "From": "2023-06-10T13:45:00.000Z"
            }
        }
        '''
        print(f'{event}')

        # TODO with Timestream


    @staticmethod
    def _HandleSubscribe(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEKf5f88769121840418de6755e4

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
            "Body": {
                "Filter": {}
            }
        }
        '''
        print(f'{event}')
        
        from MSG import MSG
        msg = MSG(event)
        domain = msg.From()
        filter = msg.Body()['Filter']
        
        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')
        subscribers.Merge(domain, { 
            'Filter': filter,
            'Status': 'SUBSCRIBED'
        })


    @staticmethod
    def _HandleUnregister(event):
        # 👉 https://quip.com/sBavA8QtRpXu#temp:C:IEK2b8247c67fae4d4487321c2e1

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        from MSG import MSG
        domain = MSG(event).From()

        from DYNAMO import DYNAMO
        subscribers = DYNAMO('SUBSCRIBERS')        
        return subscribers.Delete(domain)
    

    @staticmethod
    def _HandleUpdated(event):
        # 👉 https://quip.com/sBavA8QtRpXu/-Publisher#temp:C:IEK5a453bcdb55e4d41bcc57bbc6

        '''
        {
            "Header": {
                "From": "38ae4fa0-afc8-41b9-85ca-242fd3b735d2.dev.dtfw.org"
            }
        }
        '''
        print(f'{event}')

        from UTILS import UTILS
        id = UTILS.UUID() 

        from MSG import MSG
        msg = MSG(event)
        domain = msg.From()

        update = {
            'UpdateID': id,
            'Domain': domain,
            'Timestamp': msg.Timestamp()
        }

        from DYNAMO import DYNAMO
        updates = DYNAMO('UPDATES')
        updates.Merge(id, update)
