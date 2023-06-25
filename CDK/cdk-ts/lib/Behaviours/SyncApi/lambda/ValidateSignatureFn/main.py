#!/usr/bin/env python3

# https://github.com/kmille/dkim-verify/blob/master/verify-dkim.py
from typing import Dict, Optional
import re
import sys
from base64 import b64encode, b64decode
# import email
# import email.message
# from Crypto.Signature import PKCS1_v1_5
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from Crypto.Util.asn1 import DerSequence, DerNull, DerOctetString, DerObjectId
# import Crypto.Util
# from Crypto.Util.number import bytes_to_long, long_to_bytes
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
    pub_key = RSA.importKey(b64decode(p))
    return pub_key
    
    
def lambda_handler(event, context):   
    key = get_public_key('105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org', 'dtfw')
    return {
        'statusCode': 200,
        "body": "Success: " + key
    }
    
    