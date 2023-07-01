# 📚 Graph-Publisher

from GRAPH import GRAPH

def handler(event, context):
    return GRAPH._HandlePublisher(event)
