import pytesseract as pt
import re
from dateparser.search import search_dates
import sys
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

path = sys.argv[1]

print('Text Pre-Processing starts...')
print('Please wait...')
img_str = pt.image_to_string(path)

newstr = list(set(map(lambda x : x.strip(), img_str.split('\n'))))

newstr2 = []
for i in newstr: # create bag of words
    newstr2.extend(i.split())

newstr3 = []
for i in newstr2:
    if i.isalnum():
        continue
    else:
        newstr3.append(i)
newstr = newstr3

tags = []
for i in newstr:
    try:
        find_date = search_dates(i) 
    except:
        continue
    if find_date:
        for j in find_date:
            tags.append(j[0])

pattern1 = r"(\d{1,4}([.'’\-/])\d{1,2}([.'’\-/])\d{1,4})"
pattern2 = r"(\d{1,4}([.'’\-/\s])[ADFJMNOSadfjmnos]\w*([.'’\-/\s])\d{1,4})"
pattern3 = r"([ADFJMNOSadfjmnos]\w*\s\d{1,4}([,'’.\-/\s]*)([.'’\-/\s])\d{1,4})"
pattern4 = r"[ADFJMNOSadfjmnos]\w*\d{1,4}(['’]*)\d{1,4}"
pattern5 = r"(\d{1,4}([.'’\-/\s])\d{1,4}"

date_find = []

for i in tags:
    
    for j in (re.search(regex,i) for regex in [pattern1, pattern2, pattern3, pattern4]):
        
        if j:
            s = j.group()
            
            if s.find('.'):
                date_find.append("-".join(s.split('.')))
            
            else:
                date_find.append(s)

date_find = list(set(date_find))

dates = {}
for i in date_find:
    dates[i] = search_dates(i)[0][1].strftime("%Y-%m-%d")

print(dates)
if dates:
	print(min(dates.values()))
print('Done!!')