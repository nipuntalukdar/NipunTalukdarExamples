import sys
import json
from elasticsearch import Elasticsearch

print len(sys.argv)
es_host = '127.0.0.1:9200'
if len(sys.argv) > 1:
    es_host = sys.argv[1]

try:
    es = Elasticsearch([ es_host ])
    indexes = es.indices.get_alias('*')
    index_list = []
    for idx in indexes:
        print 'Index ' +  idx 
        index_list.append(idx)
    print 'Getting the settings...'
    index_list_comma = ','.join(index_list)
    index_settings = es.indices.get_settings(index=index_list_comma)
    for k in index_settings:
        settings = json.dumps(index_settings[k], indent=4)
        print 'Setting for ' + k
        print settings 
        print '*************************'    
    print 'Now getting the mappings for all the indexes and their types'
    index_mappings = es.indices.get_mapping(index=index_list_comma)
    for k in index_mappings:
        mappings = json.dumps(index_mappings[k]['mappings'], indent=4)
        print k, 'mapping', ':'
        print mappings, '\n*****************'
except Exception as e:
    print e
    exit(1)
