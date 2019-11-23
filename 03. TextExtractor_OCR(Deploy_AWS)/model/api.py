import io
import re
import sys
import base64
import pickle
import numpy as np
from PIL import Image
import pytesseract as pt
from dateparser.search import search_dates
from flask import Flask, request, jsonify, render_template
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

app = Flask(__name__)

def preprocessing(base64_str):
    img = Image.open(io.BytesIO(base64.decodestring(base64_str.encode())))
    img_str = pt.image_to_string(img)
    print('Preprocessing starts...')
    newstr = list(set(map(lambda x : x.strip(), img_str.split('\n'))))
    tags = []

    for i in newstr:
        try:
            find_date = search_dates(i) 
        except:
            continue
        if find_date:
            for j in find_date:
                tags.append(j[0])

    pattern1 = r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})'
    pattern2 = r'(\d{1,4}([.\-/\s])[ADFJMNOSadfjmnos]\w*([.\-/\s])\d{1,4})'
    pattern3 = r"([ADFJMNOSadfjmnos]\w*\s\d{1,4}([,.\-/\s]*)([.\-/\s])\d{1,4})"
    pattern4 = r"[ADFJMNOSadfjmnos]\w*\d{1,4}([']*)\d{1,4}"
    pattern5 = r"(\d{1,4}([.\-/\s])\d{1,4}"
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

    return dates

# use to API calls
# this simply return a dictionary object
@app.route('/extract_date',methods = ['POST'])

def predict_api():
    '''
    For direct API calls throught request
    '''
    try:
    
        data = request.get_json(force=True) # list
        if len(data) != 1:
            print("first error")
        key = list(data[0].keys())[0]
        if key != 'base_64_image_content':
            print('key not match')
        value = list(data[0].values())[0]
        
        base64_img = value.split(',')[1]
        dates = preprocessing(base64_img)

    except :
        return jsonify("something went wrong")

    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)