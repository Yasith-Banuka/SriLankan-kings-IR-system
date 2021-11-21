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
    return process(results)
    #return results
    
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

def engSearch(searchTerm):
    keyword = es.search(index='srilankan-kings', query= Queries.engKeywordSearch(searchTerm))
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
                century = re.sub(re.compile('st|nd|rd|th'),'',terms[index-1])
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
    sortFields.append("_score")
    if len(searches)>0:
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches), sort=sortFields)
        #return Queries.boolQuery(searches)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm), sort=sortFields)

def sinSearch(searchTerm):
    #keyword search to check if any records match the query exactly
    keyword = es.search(index='srilankan-kings',query= Queries.sinKeywordSearch(searchTerm),fields=["* sin"], analyzer='default')
    if keyword["hits"]["total"]["value"]>0:
        print('keyword')
        return keyword
    
    terms = searchTerm.split(' ')
    
    #search through each term
    for index, term in enumerate(terms):
        #check if term corresponds to a sort intent based on reign year
        if term in Data.sinFirstMapper:
            sortFields.append(Queries.sortByYear('asc'))
            continue
        elif term in Data.sinFinalMapper:
            print('c')
            sortFields.append(Queries.sortByYear('desc'))
            continue

        #check if query is a relationship-based query
        if re.search('.+ගේ', term):
            searches.append(Queries.fuzzyQuery('claim to the throne sin',searchTerm))
            break

        #check if term relates to a time period
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
            #check if term corresponds to a sort based on number of years of reign
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
        return es.search(index='srilankan-kings',query= Queries.boolQuery(searches), sort=sortFields)
        #return Queries.boolQuery(searches)
    return es.search(index='srilankan-kings',query= Queries.bestMatch(searchTerm), sort=sortFields)

def autocomplete(searchTerm):
    if isEnglish(searchTerm):
        results = es.search(index='srilankan-kings',query= Queries.autoComplete(searchTerm),highlight=Queries.engHighlight(),fields=["* eng"])
    else:
        results = es.search(index='srilankan-kings',query= Queries.autoComplete(searchTerm),highlight=Queries.sinHighlight(),fields=["* sin"])
    #return [results['hits']['hits'][i] for i in range(len(results['hits']['hits']))]
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
    return final

results1 = search('final rulers of polonnaruwa') 
# x = [results1['hits']['hits'][i]['_source']['name eng'] for i in range(len(results1['hits']['hits']))]
# print('\n'.join(x))
# with open("sample.json", "w",encoding='utf8') as outfile:
#     #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
#     json.dump(search('parakramabahu'), outfile, ensure_ascii=False)
    #json.dump(x, outfile, ensure_ascii=False)



            




        



