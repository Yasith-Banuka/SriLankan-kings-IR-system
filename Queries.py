def exactQuery(field,term,analyzer):
  return {"match" : {
          field : {
            "query": term,
            "analyzer": analyzer
          }
      }
    }

def fuzzyQuery(field,term,analyzer):
  return {"match" : {
          field : {
            "query" : term,
            "fuzziness": 2,
            "operator": "AND",
            "analyzer": analyzer
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

def sinKeywordSearch(term,analyzer):
  return {"multi_match" : {
        "query": term,
        "operator": "AND",
        "fields": ["name sin^3", "house sin", "kingdom sin", "Temples sin", "other constructions sin", "Inscriptions sin", "irrigation work sin", "claim to the throne sin"],
        "analyzer": analyzer
    }
  }

def engKeywordSearch(term,analyzer):
  return {"multi_match" : {
        "query": term,
        "operator": "AND",
        "fields": ["name eng^3", "house eng", "kingdom eng", "Temples eng", "other constructions eng", "Inscriptions eng", "irrigation work eng", "claim to the throne eng"],
        "analyzer": analyzer
    }
  }

def autoComplete(term,analyzer):
  return {"multi_match" : {
        "query": term,
        "type": "phrase_prefix",
        "analyzer": analyzer
    }
  }

def sinHighlight():
  return {"fields": {
      "name sin": {},
      "house sin": {},
      "kingdom sin": {},
      "Temples sin": {},
      "other constructions sin": {},
      "Inscriptions sin": {},
      "irrigation work sin": {}
    }
  }

def engHighlight():
  return {"fields": {
      "name eng": {},
      "house eng": {},
      "kingdom eng": {},
      "Temples eng": {},
      "other constructions eng": {},
      "Inscriptions eng": {},
      "irrigation work eng": {}
    }
  }


def sortByYear(order):
  return  {"_script":{  
         "type":"number",
         "script":{  
            "lang":"painless",
            "inline":"params._source.reign.lte"
         },
         "order": order
      }
   }

def bestMatch(term,analyzer):
    return {"multi_match" : {
            "query": term,
            "fuzziness": "AUTO",
            "minimum_should_match":-1,
            "analyzer": analyzer
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