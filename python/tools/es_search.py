import sys
import json
from elasticsearch import Elasticsearch

es_host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:9200'
es_index = sys.argv[2] if len(sys.argv) > 2 else 'my_index'
es_type = sys.argv[3] if len(sys.argv) > 3 else 'my_type'

try:
    out = []
    es = Elasticsearch([ es_host ])
    res = es.search(index=es_index,
    doc_type=es_type, body={"query": {"match_all": {}}}, size=100000)
    for doc in res['hits']['hits']:
        if '_source' in doc:
            if 'status' in doc['_source']:
                del doc['_source']['status']
            out.append(doc['_source'])
    if len(out) ==  res['hits']['total']:
        fp = open('out.json', 'w')
        json.dump(out, fp)
        fp.close()
except Exception as e:
    print e
    exit(1)

