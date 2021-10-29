import re
import json
def exactQuery(field,term):
    return {
        "match" : {
            field : term
        }
      }

def fuzzyQuery(field,term):
    return {
        "match" : {
            field : {
                "query" : term,
                "fuzziness": 2
            }
        }
      }

def nonEmpty(field):
    return {"regexp":{
                field: ".+"
            }
        }

def boolQuery(queryList):
    return {"bool" : {
      "must" : queryList
        }
    }

def allFields(term):
    return {"multi_match" : {
            "query": term,
            "operator":   "AND",
            "fuzziness": "AUTO" 
    }
  }

def bestMatch(term):
    return {"multi_match" : {
            "query": term,
            "fuzziness": "AUTO",
            "minimum_should_match":-1 
    }
  }

def sort(field, order):
    return {field : order}

def year(inputYear):
    return {"term" : {
        "reign" : {
            "value": inputYear
            }
        }
    }

def range(startYear, endYear):
    return {"range" : {
      "reign" : { 
        "gte" : startYear,
        "lte" : endYear
      }
    }
  }

print(type({"buckets" : ["aggregations","auto_complete","buckets"]}))

# if re.search('සියව.+', 'සියවස​'):
#     print('ක්‍රිපූ' in ['ක්‍රි.පූ.','ක්‍රිපූ','පූර්ව​'])
# a = [{'a':'b'},{'a':'w'}]
# q = {"a":1,
#     "b": a}

# print(q)



