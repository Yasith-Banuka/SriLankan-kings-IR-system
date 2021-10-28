from elasticsearch import helpers, Elasticsearch
import csv
import json
import Config

es = Elasticsearch()
if es.indices.exists(index='srilankan-kings'):
    es.indices.delete(index='srilankan-kings')
es.indices.create(index='srilankan-kings')
with open('SLRulers.json',encoding='utf8') as f:
    #reader = csv.DictReader(f)
    helpers.bulk(es, json.loads(f.read()), index='srilankan-kings')

# with open('SLRulers.csv',encoding='utf8') as f:
#     reader = csv.DictReader(f)
#     helpers.bulk(es, reader, index='srilankan-kings')

# #print(es.search(index='my-index', body={"query": {"match": {'name': 'විජය'}}}))
# #print(es.get(index='my-index', id=1))
# with open("sample.json", "w",encoding='utf8') as outfile:
#     #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
#     json.dump(es.search(index='srilankan-kings',query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
