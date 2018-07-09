import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

es_host = '127.0.0.1:9200'
indexname = 'someindex'
typename  = 'sometype'

if len(sys.argv) > 1:
    es_host = sys.argv[1]
if len(sys.argv) > 2:
    indexname = sys.argv[2]
if len(sys.argv) > 3:
    indexname = sys.argv[3]

try:
    es = Elasticsearch([ es_host ])
    ret = scan(es,
        query={"query": {"match_all": {}}},
        index=indexname,
        doc_type=typename
    )
    for i in  ret:
        print i
except Exception as e:
    print e
    exit(1)
