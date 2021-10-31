import editdistance
import Queries
import Data
import re
import json
from elasticsearch import Elasticsearch
searches=[]
sortFields=[]
es = Elasticsearch()


def synonymSearch(searchTerm, language):
    if language=='sin':
        for type in Data.sinConstructionSynonyms:
            if searchTerm in type[0]:
                print('6')
                searches.append(Queries.nonEmpty(type[1]))
                return True
        return False
    for type in Data.engConstructionSynonyms:
        if searchTerm in type:
            searches.append(Queries.nonEmpty(Data.engConstructionSynonyms[type]))
            return True
    return False

def enumSearch(searchTerm, language):
    if language=='sin':
        for i in range(2):
            for item in Data.sinEnumLists[i]:
                if editdistance.eval(item,searchTerm)<3:
                    searches.append(Queries.exactQuery(Data.sinEnumFields[i],item))
                    return True
        return False
    for i in range(2):
        for item in Data.engEnumLists[i]:
            if editdistance.eval(item,searchTerm)<3:
                searches.append(Queries.exactQuery(Data.engEnumFields[i],item))
                return True
    return False

def isEnglish(phrase):
    try:
        phrase.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def search(searchTerm):
    searches.clear()
    sortFields.clear()
    if isEnglish(searchTerm):
        results = engSearch(searchTerm.lower())
    else:
        results = sinSearch(searchTerm)
    return [results['hits']['hits'][i]['_source'] for i in range(len(results['hits']['hits']))]
    

def engSearch(searchTerm):
    keyword = es.search(index='srilankan-kings',query= Queries.allFields(searchTerm))
    if keyword["hits"]["total"]["value"]>0:
        print('keyword')
        return keyword
    terms = searchTerm.split(' ')
    for index, term in enumerate(terms):
        
        if term in Data.engFirstMapper:
            sortFields.append(Queries.sortByYear('asc'))
            continue
        elif term in Data.engFinalMapper:
            print('c')
            sortFields.append(Queries.sortByYear('desc'))
            continue
        if term in Data.engRelationshipMapper:
            print('s')
            searches.append(Queries.fuzzyQuery('claim to the throne eng',searchTerm))
            break
        if term=='century':
            print('a')
            if index>0:
                print('2')
                centuryInt = 0
                century = terms[index-1].replace(['st','nd','rd','th'],'')
                if  terms[index-1] in Data.engCenturyMapper:
                    centuryInt = Data.sinCenturyMapper.index(terms[index-1]) +1
                elif century.isdigit():
                    print('3')
                    centuryInt = int(century)
                if centuryInt>0:
                    if index+1<len(terms):
                        if terms[index+1].replace('.','')=='bc':
                            print('4')
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
                if terms[index-1] in Data.engMostMapper:
                    sortFields.append(Queries.sort('years of reign', 'desc'))
                    continue
                elif terms[index-1] in Data.engLeastMapper:
                    print('least')
                    sortFields.append(Queries.sort('years of reign', 'asc'))
                    continue
            enumSearch(term, 'eng')
    #sortFields.append("_score")
    if len(searches)>0:
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches))
        #return Queries.boolQuery(searches)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm))

def sinSearch(searchTerm):
    keyword = es.search(index='srilankan-kings',query= Queries.allFields(searchTerm))
    if keyword["hits"]["total"]["value"]>0:
        print('keyword')
        return keyword
    terms = searchTerm.split(' ')
    for index, term in enumerate(terms):
        
        if term in Data.sinFirstMapper:
            sortFields.append(Queries.sortByYear('asc'))
            continue
        elif term in Data.sinFinalMapper:
            print('c')
            sortFields.append(Queries.sortByYear('desc'))
            continue
        if re.search('.+ගේ', term):
            
            searches.append(Queries.fuzzyQuery('claim to the throne sin',searchTerm))
            break
        if re.search('සියව.+', term):
            print('a')
            if index>0:
                print('2')
                centuryInt = 0
                century = terms[index-1].replace(u'වන','')
                if  terms[index-1] in Data.sinCenturyMapper:
                    centuryInt = Data.sinCenturyMapper.index(terms[index-1]) +1
                elif century.isdigit():
                    print('3')
                    centuryInt = int(century)
                if centuryInt>0:
                    if index>1:
                        if terms[index-2] in Data.BCSynonyms:
                            print('4')
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
            if index>1:
                if terms[index-1] in Data.sinMostMapper:
                    sortFields.append(Queries.sort('years of reign', 'desc'))
                    continue
                elif terms[index-1] in Data.sinLeastMapper:
                    print('least')
                    sortFields.append(Queries.sort('years of reign', 'asc'))
                    continue
            enumSearch(term, 'sin')
    #sortFields.append("_score")
    if len(searches)>0:
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches))
        #return Queries.boolQuery(searches)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm))


#results = search('daughter of mutasiva') 
#x = [results['hits']['hits'][i]['_source'] for i in range(len(results['hits']['hits']))]
# with open("sample.json", "w",encoding='utf8') as outfile:
#     #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
#     #json.dump(es.search(index='srilankan-kings',query= sinSearch('IIIවන විජයබාහු'), sort=sortFields), outfile, ensure_ascii=False)
#     json.dump(x, outfile, ensure_ascii=False)



            




        



