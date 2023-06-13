# {
#     "Header": {
#         "Code": "dtfw.org/msg",
#         "Version": "1",
#         "From": "any-sender.com",
#         "To": "any-receiver.com",
#         "Subject": "AnyMethod",
#         "Correlation": "125a5c75-cb72-43d2-9695-37026dfcaa48",
#         "Timestamp": "2018-12-10T13:45:00.000Z",
#         "Request": {...}
#     },
#     "Body": {}
#     "Signature": < {Header, Body} signed >
# }

#!/usr/bin/python3
import argparse
import dns.resolver


def lambda_handler(event, context):
    pass
