#!/usr/bin/env python3

# https://github.com/kmille/dkim-verify/blob/master/verify-dkim.py
import re
import dns.resolver


# 👉 https://github.com/kmille/dkim-verify
# 👉 dig dtfw._domainkey.105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org txt
def get_public_key(domain: str, selector: str):
    
    # get the domain's info
    answer = dns.resolver.query(
        "{}._domainkey.{}.".format(selector, domain), "TXT"
        ).response.answer
    
    # merge multiple TXT blocks
    txt = ''
    for a in answer:
        txt = txt + a.to_text()
    txt = txt.replace('\" \"', '')
    
    # get the p= variable
    key = re.search(r'p=([\w\d/+]*)', txt).group(1)
    
    return key 
    
    
def lambda_handler(event, context):
    print(f'{event=}')
    if 'domain' not in event:
        raise Exception('Pass the [domain] arg.')
    key = get_public_key(event['domain'], 'dtfw')
    print(f'{key=}')
    return key
    
'''
{
    "domain": "105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org"
}
'''
    