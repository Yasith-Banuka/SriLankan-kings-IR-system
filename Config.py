def config():
    return {
      "settings" :{
        "analysis": {
          "analyzer": {
            "sinhala": {
              "tokenizer": "whitespace",
                "filter":[
                  "sinhala_stemmer",
                  "custom_stems"
                ]
              }
            },
            "filter": {
              "sinhala_stemmer": {
                "type": "hunspell",
                "locale": "si_LK"
              },
              "custom_stems": {
                "type": "stemmer_override",
                "rules": [
                  "පුතා, පුත්‍රයායි, පුත්‍රයාය => පුත්‍රයා",
                  "පළමුවන​, පළවන => Iවන"
                ]
              }
            }
          }
        },
      "mappings" : {
        "properties" : {
          "reign" : {
            "type": "integer_range"
          },
          "name": {
            "type": "text",
            "analyzer": "sinhala"
          },
          "claim to the throne": {
            "type": "text",
            "analyzer": "sinhala"
          }
        }
      }
    }
    


