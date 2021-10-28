import editdistance
import Queries
import re
import json
from elasticsearch import Elasticsearch
searches=[]
sort=''
es = Elasticsearch()
sinKingdoms = ['අනුරාධපුර','උපතිස්ස නුවර','කුරුණෑගල','කෝට්ටේ','ගම්පොළ','තම්බපණ්ණි','දඹදෙණිය','පොළොන්නරු','මහනුවර','යාපහුව ','සීතාවක']
engKingdoms = ['Tambapanni','Upatissa Nuwara','Anuradhapura','Polonnaruwa','Dambadeniya','Yapahuwa','Kurunegala','Gampola','Kotte','Seethawaka','Kandy']
sinHouses = ['විජය','Iවන ලම්බකර්ණ','මෝරිය','IIවන ලම්බකර්ණ','චෝළ','විජයබාහු','කාලිංග','පාණ්ඩ්‍ය','නැගෙනහිර ගංග','දිනරාජ','නායක්කර්','සිරි සඟ බෝ']
engHouses = ['Vijaya', 'Lambakanna I', 'Moriya', 'Lambakanna II', 'Chola', 'Vijayabahu', 'Kalinga', 'Pandya', 'Eastern Ganga', 'Dinajara', 'Nayak', 'Siri Sanga Bo']
sinEnumFields = ['kingdom sin','house sin']
sinEnumLists = [sinKingdoms,sinHouses]
engEnumFields = ['kingdom eng','house eng']
engEnumLists = [engKingdoms,engHouses]
BCSynonyms = ['ක්‍රි.පූ','ක්‍රිපූ','පූර්ව​']

sinConstructionSynonyms = {
    (('විහාර​','දාගැබ්','ස්ථූප​','පන්සල්','වෙහෙර​'),'Temples sin'),
    (('ලිපි','සෙල්ලිපි','සන්නස්'),'inscriptions sin'),
    (('වැව්'),'irrigation work sin'),
    (('මාලිගා','ප්‍රසාද​​','උයන්'),'other constructions sin')
}

engConstructionSynonyms = {
    (('temples'),'Temples eng'),
    (('inscriptions'),'inscriptions eng'),
    (('tanks','reservoirs'),'irrigation work eng'),
    (('Palaces', 'Gardens'),'other constructions eng')
}

sinCenturyMapper = ['පළමුවන​','දෙවන​','තුන්වන​','සිව්වන​','පස්වන​','හයවන​','හත්වන','අටවන​','නවවන​','දහවන','එකොලොස්වන','දොලොස්වන​','දහතුන්වන','දහහතරවන​','පහලොස්වන​','දහසයවන​','දහහත්වන​','දහඅටවන​','දහනවවන​']

sinFirstMapper = ['ආරම්භක','ප්‍රථම','මුල්']
sinFinalMapper = ['අවසාන','අන්තිම']

sinMostMapper = ['දීර්ඝ','	දිග', 'දිගු']
sinLeastMapper = ['කෙටි','අඩු','අල්ප​']

def search(searchTerm):
    searches.clear()
    sort=''
    if isEnglish(searchTerm):
        return engSearch(searchTerm)
    return sinSearch(searchTerm)

def sinSearch(searchTerm):
    terms = searchTerm.split()
    for index, term in enumerate(terms):
        if term in sinFirstMapper:
            sort = Queries.sort('start of reign', 'asc')
            continue
        elif term in sinFinalMapper:
            sort = Queries.sort('start of reign', 'desc')
            continue
        if re.search('.+ගේ', term):
            print('a')
            searches.append(Queries.exact('claim to the throne sin',searchTerm))
            break
        if re.search('සියව​.+', term):
            if index>1:
                centuryInt = 0
                century = terms[index-1].replace(u'වන','')
                if  terms[index-1] in sinCenturyMapper:
                    centuryInt = sinCenturyMapper.index(terms[index-1]) +1
                elif century.isdigit():
                    centuryInt = int(century)
                if centuryInt>0:
                    if index>2:
                        if terms[index-2] in BCSynonyms:
                            searches.append(Queries.range(centuryInt*(-100),(centuryInt-1)*(-100)))
                            continue
                    searches.append(Queries.range((centuryInt-1)*100,centuryInt*100))
            continue
        if term.isdigit() and int(term)>20:
            if terms[index-1] in BCSynonyms:
                searches.append(Queries.year(int(term)*-1))
            else:
                searches.append(Queries.year(int(term)))
            continue
        if not synonymSearch(term, 'sin'):
            if index>1:
                if terms[index-1] in sinMostMapper:
                    sort = Queries.sort('years of reign', 'desc')
                    continue
                elif terms[index-1] in sinLeastMapper:
                    sort = Queries.sort('years of reign', 'asc')
                    continue
            enumSearch(term, 'sin')
    if len(searches)>0:
        print('b')
        return Queries.boolQuery(searches)

with open("sample.json", "w",encoding='utf8') as outfile:
    #json.dump(es.search(index='srilankan-kings', query= {"match": {'name': 'විජය'}}), outfile, ensure_ascii=False)
    json.dump(es.search(index='srilankan-kings',query= sinSearch('මුටසීවගේ')), outfile, ensure_ascii=False)

            




        

def synonymSearch(searchTerm, language):
    if language=='sin':
        for type in sinConstructionSynonyms:
            if searchTerm in type:
                searches.append(Queries.nonEmpty(sinConstructionSynonyms[type]))
                return True
        return False
    for type in engConstructionSynonyms:
        if searchTerm in type:
            searches.append(Queries.nonEmpty(engConstructionSynonyms[type]))
            return True
    return False

def enumSearch(searchTerm, language):
    if language=='sin':
        for i in range(2):
            for item in sinEnumLists[i]:
                if editdistance.eval(item,searchTerm)<3:
                    searches.append(Queries.exact(sinEnumFields[i],item))
                    return True
        return False
    for i in range(2):
        for item in engEnumLists[i]:
            if editdistance.eval(item,searchTerm)<3:
                searches.append(Queries.exact(engEnumFields[i],item))
                return True
    return False

def isEnglish(phrase):
    try:
        phrase.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


