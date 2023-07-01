import boto3


def test():
    return 'this is a BUS test.'


events = boto3.client('events')
class BUS:
        
    # 👉 https://blog.knoldus.com/how-to-create-an-eventbridge-application-in-python/
    # 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html
    # 👉 https://boto3.amazonaws.com/v1/documentation/api/1.10.46/reference/services/events.html
    @staticmethod
    def Publish(eventBusName, source, detailType, detail):
        return events.put_events(
            Entries=[
                {
                    'Source':source,
                    'DetailType':detailType,
                    'Detail':detail,
                    'EventBusName':eventBusName
                }
            ]
    )

