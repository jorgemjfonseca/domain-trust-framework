# 📚 SyncApi.ValidateSignatureFn

from OpenSSL import crypto
#import os
#import json
#import base64

    
def lambda_handler(event, context):   
    print(f"{event=}")
    
    

'''
{
    "Message": "{\"Header\":{\"Correlation\":\"bb37d258-015c-497e-8a67-50bf244a9299\",\"Timestamp\":\"2023-06-24T23:08:24.550719Z\",\"To\":\"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org\",\"Subject\":\"AnyMethod\",\"Code\":\"dtfw.org/msg\",\"Version\":\"1\",\"From\":\"105b4478-eaa5-4b73-b2a5-4da2c3c2dac0.dev.dtfw.org\"},\"Body\":{}}",
    "PublicKey": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvIFyT1ahUEOpNftMqgVwF2jf0Zyq7q22kpi7QMo37w5y7j2byGip5YykA+LCXZZbkanLxh4GiMimTDAHQxvC/yLjQwWLJXtRndIwCtVlr09+uLp7aepL8PmNNQJhMoG8P1rp8E+jcB8lPb8G1RKAZgNyY3H/axgtOLuRNCms9IepnEa2VJZsT6peHKC9hEOBuIKw/SKKRVXgixtF05S4BdUCJ1lvXLVcRHuKbPkFzNap7JnIdc5hnSUnHv/VJSLDJj+SErP8nqomM+jR3JmsLr9aitd99nGeusNfbEIXbUaPgJxjXEkBwk6YZiWTWA61LPW/XCXtkiFKRVhgJz9HWwIDAQAB",
    "Signature": "Lw7sQp6zkOGyJ+OzGn+B1R4rCN/qcYJCtijflQu1Ayqpgxph10yS3KwA4yRhjXgUovskK7LSH+ZqhXm1bcLeMS81l1GKDVaZk3qXpNtrwRmnWrjfD1MekZrO1sRWPNBRH157INAkPWFH/Wb2LLPCAJZYwIv02BF3zKz/Zgm8z7BqOJ3ZrAOC80kTef1zhXNXUMQ/HBrspUTx0NFiMi+dXZMJ69ylxGaAjALMLmcMwFqH2D5cWqX5+eMx0zv2tMh73e8xQqxOr+YLUkO7JjK56KbCUk0HYGUbL5co9eyQMYCGyDtn0G2FqSK9h8BJ1YW3LQmWWTGa/kWDxPjHR3iNyg=="
}
'''