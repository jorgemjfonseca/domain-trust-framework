# 📚 Graph-Consume

from GRAPH import GRAPH

def handler(event, context):
    return GRAPH._HandleConsumer(event)
