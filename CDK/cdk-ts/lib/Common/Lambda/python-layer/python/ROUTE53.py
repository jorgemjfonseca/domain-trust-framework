import boto3
import urllib.parse


def test():
    return 'this is a ROUTE53 test.'


r53 = boto3.client('route53')
class ROUTE53:
    

    def __init__(self, hosted_zone_id):
       print(f'ROUTE53()')
       self._hosted_zone_id = hosted_zone_id
        

    def NS(self):
        print(f'ROUTE53.NS()')
        result=r53.list_resource_record_sets(HostedZoneId=self._hosted_zone_id)
        
        for r in result["ResourceRecordSets"]:
            if r["Type"] == 'NS':
                print (f'NS.Return: {r=}')
                return r
                
        raise Exception('No record NS found')
    

    def Domain(self):
        print(f'ROUTE53.Domain()')
        ns = self.NS()
        return ns['Name']
    

    def NameServers(self):
        print(f'ROUTE53.NameServers()')
        ns = self.NS()
        servers = []
        for s in ns['ResourceRecords']:
            servers.append(s['Value'])
        return servers
    

    def NameServerList(self):
        print(f'ROUTE53.NameServerList()')
        servers = self.NameServers()
        serverList = ','.join(servers)
        return serverList

        
    # 👉 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_dnssec.html#            
    # 👉 https://docs.aws.amazon.com/Route53/latest/APIReference/API_GetDNSSEC.html
    # 👉 https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-enable-signing.html
    def DX(self, unquoted=False):
        print(f'ROUTE53.DX()')

        resp = r53.get_dnssec(
            HostedZoneId = self._hosted_zone_id
        )
        print(f'{resp=}')

        ret = resp['KeySigningKeys'][0]['DSRecord']
        print(f'{ret}')

        if unquoted:
            return ret
        
        return urllib.parse.quote_plus(ret)
    

    def UpdateRecord(self, record_name, value):
        ''' https://stackoverflow.com/questions/38554754/cant-update-dns-record-on-route-53-using-boto3 '''

        print(f'ROUTE53.UpdateRecord()')
            
        changes = [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": record_name,
                    "Type": "TXT",
                    "TTL": 60,
                    "ResourceRecords": [
                        {
                            "Value": value
                        },
                    ],
                }
            },
        ]
        print(f'{changes}')
        
        r53.change_resource_record_sets(
            HostedZoneId = self._hosted_zone_id,
            ChangeBatch = {
                "Comment": "Automatic DNS update",
                "Changes": changes
            })
        
