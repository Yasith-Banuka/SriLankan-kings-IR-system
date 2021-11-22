# Sri Lankan kings IR system

This is an Information retrieval system for Sri Lankan rulers built using elasticsearch and flask. It supports Sinhala and English.

<br/>

# Running the system

## Prerequisites

Elasticsearch

Python 3

Flask

Beautiful soup (python library)

editdistnce (python library)

<br/>

## How to execute

1. If it is the first time running the system, Copy contents of 'Config' folder to {elasticsearch root}/config 

2. Start up an elasticsearch server on the default port

3. Open command line

4. Navigate to the root folder

5. If it is the first time running the system, execute "python loader.py"

6. Execute "python app.py"

7. Visit [localhost:5000](localhost:5000)

<br/>

# Repository structure

    ├── Config - Elasticsearch files to be copied to {elasticsearch root}/config    
    ├── Data - Data about the rulers                  
        ├── Raw
        └── Cleaned
    ├── Templates - UI                 
    ├── app.py - Flask app
    ├── Config.py - Elasticsearch index configuration and settings
    ├── Data.py - Data for the search algorithm
    ├── Queries.py - Elasticsearch queries for searching
    ├── Scraper.ipynb - Data scraping functionality
    └── Search.py - Search algorithms

<br/>

# Data

The system holds the following data about the rulers (Some data may not be available for some rulers)

- Name*
- House*
- Kingdom*
- Reigning period
- No. of years of reign
- Temples built*
- Irrigation work done*
- Inscriptions done*
- Other constructions*
- Claim to the throne*
- Discription

*Available in Sinhala and English

Data was scraped using the Beautiful soup library, from [wikipedia](https://en.wikipedia.org/wiki/List_of_Sri_Lankan_monarchs) and data was added from other sources.
The data was cleaned manually as language errors were present in some records.

<br/>

# Features


Bilingual - Both searching and results are avilable in Sinhala and English and can switch back and forth seamlessly.

Autocomplete - The UI allows to complete your query based on what has already been typed

Faceted search - Results can be filtered based on different fields

Compound intent classification - The system can handle multiple intents and provide reults that cater to them

Misspelling handling - Spelling mistakes are handled using fuzzy queries and edit-distance checking

Synonym adaption - Usage of synonyms is accomodated so as to not hinder searching

<br/>

## Inspiration & ideas taken from

https://github.com/iTharindu/SinhalaSongSearch

https://github.com/soumilshah1995/AutoComplete-Input-Elastic-Search-Python