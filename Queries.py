import re
import json
def exact(field,term):
    return {
        "match" : {
            field : term
        }
      }

def boolQuery(queryList):
    return {"bool" : {
      "must" : queryList
        }
    }



# a = [{'a':'b'},{'a':'w'}]
# q = {"a":1,
#     "b": a}

# print(q)

