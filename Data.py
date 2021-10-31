sinKingdoms = ['අනුරාධපුර','උපතිස්ස නුවර','කුරුණෑගල','කෝට්ටේ','ගම්පොළ','තම්බපණ්ණි','දඹදෙණිය','පොළොන්නරු','මහනුවර','යාපහුව ','සීතාවක']
engKingdoms = ['Tambapanni','Upatissa Nuwara','Anuradhapura','Polonnaruwa','Dambadeniya','Yapahuwa','Kurunegala','Gampola','Kotte','Seethawaka','Kandy']

sinHouses = ['විජය','Iවන ලම්බකර්ණ','මෝරිය','IIවන ලම්බකර්ණ','චෝළ','විජයබාහු','කාලිංග','පාණ්ඩ්‍ය','නැගෙනහිර ගංග','දිනරාජ','නායක්කර්','සිරි සඟ බෝ']
engHouses = ['Vijaya', 'Lambakanna I', 'Moriya', 'Lambakanna II', 'Chola', 'Vijayabahu', 'Kalinga', 'Pandya', 'Eastern Ganga', 'Dinajara', 'Nayak', 'Siri Sanga Bo']

sinEnumFields = ['kingdom sin','house sin']
sinEnumLists = [sinKingdoms,sinHouses]

engEnumFields = ['kingdom eng','house eng']
engEnumLists = [engKingdoms,engHouses]

BCSynonyms = ['ක්‍රි.පූ.','ක්‍රිපූ','පූර්ව​']

sinConstructionSynonyms = [
    (('විහාර​','දාගැබ්','ස්ථූප​','පන්සල්','වෙහෙර​'),'Temples sin'),
    (('ලිපි','සෙල්ලිපි','සන්නස්'),'inscriptions sin'),
    (('වැව්'),'irrigation work sin'),
    (('මාලිගා','ප්‍රසාද​​','උයන්'),'other constructions sin')
]

engConstructionSynonyms = {
    (('temples'),'Temples eng'),
    (('inscriptions'),'inscriptions eng'),
    (('tanks','reservoirs'),'irrigation work eng'),
    (('Palaces', 'Gardens'),'other constructions eng')
}

sinCenturyMapper = ['පළමුවන​','දෙවන​','තුන්වන​','සිව්වන​','පස්වන​','හයවන​','හත්වන','අටවන​','නවවන​','දහවන','එකොලොස්වන','දොලොස්වන​','දහතුන්වන','දහහතරවන​','පහලොස්වන​','දහසයවන​','දහහත්වන​','දහඅටවන​','දහනවවන​']
engCenturyMapper = ['first','second','third','fourth','fifth','sixth','seventh','eighth','nineth','tenth','eleventh','twelvth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth','eighteenth','nineteenth']


sinFirstMapper = ['ආරම්භක','ප්‍රථම','මුල්']
sinFinalMapper = ['අවසාන','අන්තිම']

engFirstMapper = ['first','starting','beginning']
engFinalMapper = ['last','final']

sinMostMapper = ['දීර්ඝ','	දිග', 'දිගු']
sinLeastMapper = ['කෙටි','අඩු','අල්ප​']

engMostMapper = ['longest','most']
engLeastMapper = ['shortest','least']

engRelationshipMapper = ['sister', 'widow', 'minister', 'father-in-law', 'brother', 'son-in-law', 'daughter', 'heir', 'law', 'brother-in-law', 'father', 'sword-bearer', 'son', "brother", 'sub-king', 'grandson', 'husband', 'nephew.', 'prince', 'uncle', 'queen', 'general', 'chief', 'cousin']
sinRelationshipMapper = [["මස්සිනා", "දියණිය", "අසිපත්ධාරියායි.", "අමාත්‍යවරයකු", "සත්‍ය", "පුත්‍රයායි.", "සොහොයුරා", "දෙවන", "සිංහල", "පුත්‍රයායි.කාශ්‍යපගේ", "සොයුරියට", "වැඩිමහල්", "බෑණායි.කස්සපගේ", "අගමෙහෙසියයි", "සොහොයුරෙක.", "උප-රජෙකි", "මස්සිනායි.", "බාල", "මුණුපුරා", "සහ", "මුණුපුරා", "පුත්‍රය", "වැන්දඹුව", "බෑණා", "සොහොයුරා", "අග්‍රාමාත්‍යවරයා", "පියා", "මාමණ්ඩිය", "සෙන්පතිය.", "සොයුරිය.", "ඥාති", "සහෝදරයා", "ප්‍රධාන", "‍බාල", "වැඩිමහල්ම", "උප-රජ.", "බෑණා", "දොරටුපාලකයායි."]]