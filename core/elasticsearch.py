from elasticsearch import Elasticsearch
from django.contrib.auth.models import User

es = Elasticsearch([{'host': 'localhost', 'port': 8000, 'scheme': "https"}])

# def index_users():
#     users = User.objects.all()
#     for user in users:
#         es.index(index='users_index', id=user.id, body={'username': user.username})
#         print(es)

def search_users(query):
    print('*'*25)
    users = User.objects.all()
    for user in users:
        print('*'*25)
        es.index(index='users_index', id=user.id, body={'username': user.username})
        print(es)
    body = {
        "query": {
            "prefix": {"username": query}
        }
    }
    results = es.search(index='users_index', body=body)
    return results['hits']['hits']