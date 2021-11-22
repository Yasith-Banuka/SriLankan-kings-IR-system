import editdistance
import Queries
import Data
import re
from elasticsearch import Elasticsearch

searches=[]
sortFields=[]
es = Elasticsearch()

#Function to check for misspeling and availability in a list
def fuzzySearch(term, list):
    for item in list:
        if editdistance.eval(item,term)<2:
            return True
    return False

#Function to check for synonyms in construction fields
def synonymSearch(searchTerm, language):
    if language=='sin':
        for key, value in Data.sinConstructionSynonyms:
            if fuzzySearch(searchTerm, key):
                searches.append(Queries.nonEmpty(value))
                return True
        return False
    for key, value in Data.engConstructionSynonyms:
        if fuzzySearch(searchTerm, key):
            searches.append(Queries.nonEmpty(value))
            return True
    return False

#Function to check for availability in house or kingdom fields
def enumSearch(searchTerm, language):
    if language=='sin':
        for i in range(2):
            for item in Data.sinEnumLists[i]:
                if editdistance.eval(item,searchTerm)<2:
                    searches.append(Queries.exactQuery(Data.sinEnumFields[i],item, Data.sinAnalyzer))
                    return True
        return False
    for i in range(2):
        for item in Data.engEnumLists[i]:
            if editdistance.eval(item,searchTerm)<2:
                searches.append(Queries.exactQuery(Data.engEnumFields[i],item,Data.engAnalyzer))
                return True
    return False

#Function to check for the language of the query
def isEnglish(phrase):
    try:
        phrase.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

#Main search function
def search(searchTerm):
    searches.clear()
    sortFields.clear()
    if isEnglish(searchTerm):
        results = engSearch(searchTerm.lower())
    else:
        results = sinSearch(searchTerm)
    return process(results)

#Function for post-processing. Adds affixes to reiging period
def process(results):
    resultList = [results['hits']['hits'][i]['_source'] for i in range(len(results['hits']['hits']))]

    for index,res in enumerate(resultList):

        sinStart = str(abs(res['reign']['gte']))
        engStart = str(abs(res['reign']['gte']))
        if res['reign']['gte']<0:
            sinStart = 'ක්‍රි.පූ. '+ sinStart
            engStart = engStart + ' B.C.'
        elif res['reign']['gte']<100:
            sinStart = 'ක්‍රි.ව. '+ sinStart
            engStart = engStart + ' A.D.'

        sinEnd = str(abs(res['reign']['lte']))
        engEnd = str(abs(res['reign']['lte']))
        if res['reign']['lte']<0:
            sinEnd = 'ක්‍රි.පූ. ' + sinEnd
            engEnd = engEnd + ' B.C.'
        elif res['reign']['lte']<100:
            sinStart = 'ක්‍රි.ව. '+ sinStart
            engStart = engStart + ' A.D.'

        sinReign =  sinStart+ ' - '+ sinEnd
        engReign =  engStart + ' - '+ engEnd
        resultList[index]['reign sin'] = sinReign
        resultList[index]['reign eng'] = engReign
    return resultList

#Function for english searching
def engSearch(searchTerm):
    keyword = es.search(index='srilankan-kings', query= Queries.engKeywordSearch(searchTerm,Data.engAnalyzer))
    if keyword["hits"]["total"]["value"]>0:
        return keyword
    terms = searchTerm.split(' ')
    for index, term in enumerate(terms):
        
        if fuzzySearch(term, Data.engFirstMapper):
            sortFields.append(Queries.sortByYear('asc'))
            continue
        if fuzzySearch(term, Data.engFinalMapper):
            sortFields.append(Queries.sortByYear('desc'))
            continue
        if fuzzySearch(term, Data.engRelationshipMapper):
            searches.append(Queries.fuzzyQuery('claim to the throne eng',searchTerm,Data.engAnalyzer))
            break
        if editdistance.eval(term,'century')<2:
            if index>0:
                centuryInt = 0
                century = re.sub(re.compile('st|nd|rd|th'),'',terms[index-1])
                if  terms[index-1] in Data.engCenturyMapper:
                    centuryInt = Data.sinCenturyMapper.index(terms[index-1]) +1
                elif century.isdigit():
                    centuryInt = int(century)
                if centuryInt>0:
                    if index+1<len(terms):
                        if terms[index+1].replace('.','')=='bc':
                            searches.append(Queries.range(centuryInt*(-100),(centuryInt-1)*(-100)))
                            continue
                    searches.append(Queries.range((centuryInt-1)*100,centuryInt*100))
            continue
        if term.isdigit():
            if index+1<len(terms):
                if terms[index+1].replace('.','')=='bc':
                    searches.append(Queries.year(int(term)*-1))
                if terms[index+1].replace('.','')=='ad':
                    searches.append(Queries.year(int(term)))
            if int(term)>20:
                searches.append(Queries.year(int(term)))
            continue
        if not synonymSearch(term, 'eng'):
            if index>1:
                if fuzzySearch(terms[index-1],Data.engMostMapper):
                    sortFields.append(Queries.sort('years of reign', 'desc'))
                    continue
                elif fuzzySearch(terms[index-1],Data.engLeastMapper):
                    sortFields.append(Queries.sort('years of reign', 'asc'))
                    continue
            enumSearch(term, 'eng')
    sortFields.append("_score")
    if len(searches)>0:
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches), sort=sortFields)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm,Data.engAnalyzer), sort=sortFields)

#Function for Sinhala searching
def sinSearch(searchTerm):
    #keyword search to check if any records match the query exactly
    keyword = es.search(index='srilankan-kings',query= Queries.sinKeywordSearch(searchTerm,Data.sinAnalyzer), fields=["* sin"])
    if keyword["hits"]["total"]["value"]>0:
        return keyword
    
    terms = searchTerm.split(' ')
    
    #search through each term
    for index, term in enumerate(terms):
        #check if term corresponds to a sort intent based on reign year
        if fuzzySearch(term, Data.sinFirstMapper):
            sortFields.append(Queries.sortByYear('asc'))
            continue
        if fuzzySearch(term, Data.sinFinalMapper):
            sortFields.append(Queries.sortByYear('desc'))
            continue

        #check if query is a relationship-based query
        if fuzzySearch(term, Data.sinRelationshipMapper):
            searches.append(Queries.fuzzyQuery('claim to the throne sin',searchTerm,Data.sinAnalyzer))
            break

        #check if term relates to a time period
        if re.search('සියව.+', term):
            if index>0:
                centuryInt = 0
                century = terms[index-1].replace(u'වන','')
                if  terms[index-1] in Data.sinCenturyMapper:
                    centuryInt = Data.sinCenturyMapper.index(terms[index-1]) +1
                elif century.isdigit():
                    centuryInt = int(century)
                if centuryInt>0:
                    if index>1:
                        if terms[index-2] in Data.BCSynonyms:
                            searches.append(Queries.range(centuryInt*(-100),(centuryInt-1)*(-100)))
                            continue
                    searches.append(Queries.range((centuryInt-1)*100,centuryInt*100))
            continue
        if term.isdigit() and int(term)>20:
            if terms[index-1] in Data.BCSynonyms:
                searches.append(Queries.year(int(term)*-1))
            else:
                searches.append(Queries.year(int(term)))
            continue

        if not synonymSearch(term, 'sin'):
            #check if term corresponds to a sort based on number of years of reign
            if index>1:
                if fuzzySearch(terms[index-1],Data.sinMostMapper):
                    sortFields.append(Queries.sort('years of reign', 'desc'))
                    continue
                elif fuzzySearch(terms[index-1],Data.sinLeastMapper):
                    sortFields.append(Queries.sort('years of reign', 'asc'))
                    continue
            enumSearch(term, 'sin')
    sortFields.append("_score")
    if len(searches)>0:
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches), sort=sortFields)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm,Data.sinAnalyzer), sort=sortFields)

#Function for autocomplete functionality
def autocomplete(searchTerm):
    if isEnglish(searchTerm):
        results = es.search(index='srilankan-kings',query= Queries.autoComplete(searchTerm,Data.engAnalyzer),highlight=Queries.engHighlight(),fields=["* eng"])
    else:
        results = es.search(index='srilankan-kings',query= Queries.autoComplete(searchTerm,Data.sinAnalyzer),highlight=Queries.sinHighlight(),fields=["* sin"])

    candidates = []
    for res in results['hits']['hits']:
        try:
            highlights = res['highlight']
        except:
            continue
        candidates.extend([item for sublist in list(highlights.values()) for item in sublist])
    final = []
    for candidate in candidates:
        if ',' in candidate:
            for i in candidate.split(','):
                if '<em>' in i:
                    final.append(i.replace('<em>','').replace('</em>',''))
                    break
        else:
            final.append(candidate.replace('<em>','').replace('</em>',''))
    return list(set(final))




            




        



