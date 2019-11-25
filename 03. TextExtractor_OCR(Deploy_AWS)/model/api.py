import io
import re
import cv2
import sys
import base64
import numpy as np
from PIL import Image
import pytesseract as pt
from dateutil.parser import parse
from flask import Flask, request, jsonify, render_template
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

app = Flask(__name__)

class date_finder():
    
    def __init__(self):
        self.pattern1 = r"(\d{1,4}([.'’\-/])\d{1,2}([.'’\-/])\d{1,4})"
        self.pattern2 = r"(\d{1,4}([.'’\-/\s])[ADFJMNOSadfjmnos]\w*([.'’\-/\s]*)\d{1,4})"
        self.pattern3 = r"([ADFJMNOSadfjmnos]\w*\s\d{1,4}([,'’.\-/\s]*)([.'’\-/\s])\d{1,4})"
        self.pattern4 = r"[ADFJMNOSadfjmnos]\w*\d{1,4}(['’]*)\d{1,4}"
        self.pattern5 = r"(\d{1,4}([.'’\-/\s])\d{1,4}"
        self.dates = []
        
    def find_date(self, img_str):
        date_find = []
        for i in img_str:
            for j in (re.search(regex,i) for regex in [self.pattern1, self.pattern2, self.pattern3, self.pattern4]):
                if j:
                    s = j.group()
                    if s.find('.'):
                        date_find.append("-".join(s.split('.')))
                    else:
                        date_find.append(s)

        date_find = list(set(date_find))
        for i in date_find:
            try:
                i = i.replace("’","'")
                i = i.replace("’’","'")
                i = i.replace('"',"'")
                i = parse(i).strftime("%Y-%m-%d")
                if 2010 < int(i[:4]) < 2020:
                    self.dates.append(i)   
            except:
                continue
                
    def extract_img_str(self,base64_str):
        
        config = ("-l eng --oem 1 --psm 3")
        gaussian_filter = (3,3) 
        img = Image.open(io.BytesIO(base64.decodestring(base64_str.encode())))
        img = np.array(img)
        img = cv2.resize(img, None, fx = 3, fy = 3, interpolation=cv2.INTER_CUBIC) 
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, gaussian_filter, 0)
        img_str_1 = pt.image_to_string(Image.fromarray(img_blur),lang ="eng",config=config)
        img_str_1 = list(set(map(lambda x : x.strip(), img_str_1.split('\n'))))
        self.find_date(img_str_1)
        if self.dates:
            return None
    
        img_str_2 = pt.image_to_string(Image.fromarray(img), lang='eng',config=config)
        img_str_2 = list(set(map(lambda x : x.strip(), img_str_2.split('\n'))))
        self.find_date(img_str_2)
        if self.dates:
            return None 
    
        ret,th1 = cv2.threshold(img_blur, 100, 225, cv2.THRESH_BINARY)
        img_str_3 = pt.image_to_string(Image.fromarray(th1), lang = 'eng',config=config)
        img_str_3 = list(set(map(lambda x : x.strip(), img_str_3.split('\n'))))
        self.find_date(img_str_3)
        if self.dates:
            return None 
    
        img_ad_thres = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img_str_4 = pt.image_to_string(Image.fromarray(img_ad_thres),lang='eng',config=config)
        img_str_4 = list(set(map(lambda x : x.strip(), img_str_4.split('\n'))))
        self.find_date(img_str_4)
        if self.dates:
            return None 
        return None

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
        obj = date_finder()
        obj.extract_img_str(base64_img)
        dates = {}
        if obj.dates:
            dates['date'] = obj.dates[0]
        else:
            dates['date'] = 'None'
    except Exception as e:
        print(e)
        return jsonify("something went wrong")

    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)