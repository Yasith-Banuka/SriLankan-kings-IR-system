sinKingdoms = [
'අනුරාධපුර',
'උපතිස්ස නුවර',
'කුරුණෑගල',
'කෝට්ටේ',
'ගම්පොළ',
'තම්බපණ්ණි',
'දඹදෙණිය',
'පොළොන්නරු',
'මහනුවර',
'යාපහුව ',
'සීතාවක']



# def search(searchTerm):
#     terms = searchTerm.split()
#     for term in terms:
#         if term in sinKingdoms:

import editdistance

print(editdistance.eval('අනුරාධපුර','අනුරාධර'))