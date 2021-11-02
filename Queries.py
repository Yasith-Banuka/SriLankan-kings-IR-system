import re
import json
def exactQuery(field,term):
  return {"match" : {
          field : term
      }
    }

def fuzzyQuery(field,term):
  return {"match" : {
          field : {
            "query" : term,
            "fuzziness": 2,
            "operator": "AND"
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
        "operator": "AND",
        "fuzziness": "AUTO" 
    }
  }

def autoComplete(term):
  return {"multi_match" : {
        "query": term,
        "type": "phrase_prefix"
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

#print(type({"buckets" : ["aggregations","auto_complete","buckets"]}))

# if re.search('සියව.+', 'සියවස​'):
#     print('ක්‍රිපූ' in ['ක්‍රි.පූ.','ක්‍රිපූ','පූර්ව​'])
# a = [{'a':'b'},{'a':'w'}]
# q = {"a":1,
#     "b": a}

# print(q)

import pandas as pd

# df = pd.read_csv('SLRulers.csv',encoding='utf8')
# terms = []
# for index, row in df.iterrows():
#   try:
#     for index,term in enumerate(row['claim to the throne sin'].replace('.','  ').split()):
#       if re.search('.+\ගේ', term):
#         terms.append(row['claim to the throne sin'].split()[index+1])
#         break
#   except AttributeError:
#     continue
# #print(set(terms))
# with open("sample.json", "w",encoding='utf8') as outfile:
#     #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
#     json.dump(list(set(terms)), outfile, ensure_ascii=False)

print(re.sub(re.compile('st|nd|rd|th'),'','2st'))