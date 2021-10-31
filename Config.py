def config():
    return {
      "settings" :{
        "analysis": {
          "analyzer": {
            "default": {
              "tokenizer": "standard",
              "filter":[
                "sinhala_stemmer",
                "sinhala_synonym",
                "sinhala_stopwords"
              ]
            },
            "default_search": {
              "tokenizer": "standard",
              "filter":[
                "sinhala_stemmer",
                "sinhala_synonym",
                "sinhala_stopwords"
              ]                
            },
            "english": {
              "tokenizer": "lowercase",
              "filter":[
                "stemmer",
                "english_synonym",
                "stop"
              ]                
            }
          },
            "filter": {
              "sinhala_stemmer": {
                "type": "hunspell",
                "locale": "si_LK"
              },
              "sinhala_synonym": {
                "type": "synonym",
                "synonyms_path": "srilankankings-filters/sinhala_synonyms.txt"
              },
              "sinhala_stopwords": {
                "type": "stop",
                "stopwords_path": "srilankankings-filters/sinhala_stopwords.txt"
              },
              "english_synonym": {
                "type": "synonym",
                "synonyms_path": "srilankankings-filters/english_synonyms.txt"
              }
            }
          }
        },
"mappings" : {
      "properties" : {
        "Inscriptions eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "Temples eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "claim to the throne eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "end of reign" : {
          "type" : "text"
        },
        "house eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "irrigation work eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "kingdom eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "name eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "other constructions eng" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          },
          "analyzer" : "english",
          "search_analyzer" : "english"
        },
        "reign" : {
          "type" : "integer_range"
        },
        "start of reign" : {
          "type" : "text"
        },
        "years of reign" : {
          "type" : "long"
        }
      }
    }
  }
  
    


