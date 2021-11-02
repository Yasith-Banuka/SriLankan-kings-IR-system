from elasticsearch import helpers, Elasticsearch
import json
import Config

es = Elasticsearch()
if es.indices.exists(index='srilankan-kings'):
    es.indices.delete(index='srilankan-kings')
es.indices.create(index='srilankan-kings', body=Config.config())
with open('SLRulers.json',encoding='utf8') as f:
    #reader = csv.DictReader(f)
    helpers.bulk(es, json.loads(f.read()), index='srilankan-kings')

