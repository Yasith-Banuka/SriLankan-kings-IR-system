from elasticsearch import helpers, Elasticsearch
import csv
import json
import Config

es = Elasticsearch()
if es.indices.exists(index='srilankan-kings'):
    es.indices.delete(index='srilankan-kings')
es.indices.create(index='srilankan-kings', body=Config.config())
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
#     json.dump(es.search(index='srilankan-kings',query= {"match": {'name sin': 'විජය'}}), outfile, ensure_ascii=False)
# ss=es.search(index='srilankan-kings',body=
# {
#             "query": {
#                 "match_phrase_prefix": {
#                     "kingdom eng": {
#                         "query": "A"
#                     }
#                 }
#             },
#             "aggs": {
#                 "auto_complete": {
#                     "terms": {
#                         "field": "kingdom eng.keyword",
#                         "order": {
#                             "_count": "desc"
#                         },
#                         "size": 25
#                     }
#                 }
#             }
#         })
# sss = ss["aggregations"]["auto_complete"]["buckets"]
# sss.extend(sss)
# print(len(ss["aggregations"]["auto_complete"]["buckets"]))
# print(len(sss))
# ss["aggregations"]["auto_complete"]["buckets"] = sss
# # with open("sample.json", "w",encoding='utf8') as outfile:
# #     #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
# #     json.dump(ss, outfile, ensure_ascii=False)
# print(len(ss["aggregations"]["auto_complete"]["buckets"]))
