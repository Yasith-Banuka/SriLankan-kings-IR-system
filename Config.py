def config():
    return {
      "settings" :{
        "analysis": {
          "analyzer": {
            "default": {
              "tokenizer": "standard",
              "filter":[
                "sinhala_stemmer",
                "synonym",
                "stopwords"

              ]
            },
            "default_search": {
              "tokenizer": "whitespace",
              "filter":[
                "sinhala_stemmer",
                "synonym",
                "stopwords"
              ]                
              }
            },
            "filter": {
              "sinhala_stemmer": {
                "type": "hunspell",
                "locale": "si_LK"
              },
              "synonym": {
                "type": "synonym",
                "synonyms_path": "srilankankings-filters/synonyms.txt"
              },
              "stopwords": {
                "type": "stop",
                "stopwords_path": "srilankankings-filters/stopwords.txt"
              }
            }
          }
        },
"mappings" : {
      "properties" : {
        "Inscriptions" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "Temples built" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "claim to the throne" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "end of reign" : {
          "type" : "long"
        },
        "house" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "irrigation work" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "kingdom eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "kingdom sin" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "other constructions" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "default"
        },
        "reign" : {
          "type" : "integer_range"
        },
        "start of reign" : {
          "type" : "long"
        }
      }
    }
  }
  
    


