try:
    from flask import app,Flask
    from flask_restful import Resource, Api, reqparse
    import elasticsearch
    from elasticsearch import Elasticsearch
    import datetime
    import concurrent.futures
    import requests
    import json
except Exception as e:
    print("Modules Missing {}".format(e))


app = Flask(__name__)
api = Api(app)

#------------------------------------------------------------------------------------------------------------

NODE_NAME = 'srilankan-kings'
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#------------------------------------------------------------------------------------------------------------


"""
{
"wildcard": {
    "Kingdom_eng": {
        "value": "{}*".format(self.query)
    }
}
}

"""


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.baseQuery ={
            "_source": [],
            "size": 0,
            "min_score": 0.5,
            "query": {
                "match_phrase_prefix": {
                    "name eng": {
                        "query": "{}".format(self.query)
                    }
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "name eng.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }
        self.baseQuery2 ={
            "_source": [],
            "size": 0,
            "min_score": 0.5,
            "query": {
                "match_phrase_prefix": {
                    "house eng": {
                        "query": "{}".format(self.query)
                    }
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "house eng.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

    def get(self):
        fin=[]
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        
        aggs = res["aggregations"]["auto_complete"]["buckets"]
        fin.extend(aggs)
        res2 = es.search(index=NODE_NAME, size=0, body=self.baseQuery2)
        aggs2 = res2["aggregations"]["auto_complete"]["buckets"]
        fin.extend(aggs2)
        #res["aggregations"]["auto_complete"]["buckets"] = fin
        #print(res["aggregations"]["auto_complete"]["buckets"],flush=False)
        return {"buckets" : fin}


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
