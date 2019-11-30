# Import required libraries
import io
import re
import cv2
import sys
import base64
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract as pt
from dateutil.parser import parse
from flask import Flask, request, jsonify, render_template
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# creating flask object
app = Flask(__name__)

# Defining class which perform image preprocessing and date extraction
class DateFinder():
    
    def __init__(self):
        self.pattern1 = r"(\d{1,4}([.'’~\-/])\d{1,2}([.'’~\-/])\d{1,4})"
        self.pattern2 = r"(\d{1,4}([.'’~\-/\s])[ADFJMNOSadfjmnos]\w*([.'’~\-/\s]*)\d{1,4})"
        self.pattern3 = r"([ADFJMNOSadfjmnos]\w*\s\d{1,4}([,'’~.\-/\s]*)([.'’~\-/\s])\d{1,4})"
        self.pattern4 = r"[ADFJMNOSadfjmnos]\w*\d{1,4}(['’]*)\d{1,4}"
        self.pattern5 = r"(\d{1,4}([.'’~\-/\s])\d{1,4}"
        self.dates = []
        
    def find_date(self, img_str):
    	'''
		img_str : extracted string from image using pytesseract.image_to_string()
    	'''
        date_find = []
        for i in img_str:
        	# Extract all type to date format which present in img_str string
            for j in (re.search(regex,i) for regex in [self.pattern1, self.pattern2, self.pattern3, self.pattern4]):
                if j:
                    s = j.group()
                    if s.find('.'):
                        date_find.append("-".join(s.split('.')))
                    else:
                        date_find.append(s)
        
        # remove duplicates
        date_find = list(set(date_find))
        for i in date_find:
            try:
                i = i.replace("’","'")
                i = i.replace("’’","'")
                i = i.replace('"',"'")
                i = i.replace('~',"-")
                i = parse(i).strftime("%Y-%m-%d")
                if 1999 < int(i[:4]) < 2020:
                    self.dates.append(i)   
            except:
                continue
                
    def extract_img_str(self,base64_str):
        '''
        base64_str : base64 form of an Image
        info:
        # Instead of passing single image. We use STACKING ENSEMBLE TECHNIQUE.
        # Passing an image with 3 different filters then pass all 3 images
        # with 4 different preprocessed techique. It results we get total 
        # 12 different outputs from all of them we select according to 
        # maximum votings.
        ###########################################################################################################
        # Image_1_1*[3,3] + Image_1_2*[3,3] + Image_1_3*[3,3] + Image_1_4*[3,3] = date1_1,date1_2,date1_3,date1_4 #
        # Image_2_1*[3,3] + Image_2_2*[3,3] + Image_2_3*[3,3] + Image_2_4*[3,3] = date2_1,date2_2,date2_3,date2_4 #
        # Image_3_1*[3,3] + Image_3_2*[3,3] + Image_3_3*[3,3] + Image_3_4*[3,3] = date3_1,date3_2,date3_3,date3_4 #
        # max_vote(date1,date2,date3) ====> DATE                                                                  #
        ###########################################################################################################
       
        '''
        # Converting base64_str into image
        img = Image.open(io.BytesIO(base64.decodestring(base64_str.encode())))
        img = np.array(img)
        img = cv2.resize(img, None, fx = 2.5, fy = 2.5, interpolation=cv2.INTER_CUBIC) 
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = ("-l eng --oem 1 --psm 3")
        filters = [3,5,7]
        for i in filters:
            st = 'With ({0},{0}) '.format(i) + 'filter and '
            gaussian_filter = (i,i)
            img_blur = cv2.GaussianBlur(img_gray, gaussian_filter, 0)
            img_str_1 = pt.image_to_string(Image.fromarray(img_blur),lang ="eng",config=config)
            img_str_1 = list(set(map(lambda x : x.strip(), img_str_1.split('\n'))))
            self.find_date(img_str_1)
            if self.dates:
                print(st+'First preprocessed : ',self.dates[-1])
                continue

            img_str_2 = pt.image_to_string(Image.fromarray(img), lang='eng',config=config)
            img_str_2 = list(set(map(lambda x : x.strip(), img_str_2.split('\n'))))
            self.find_date(img_str_2)
            if self.dates:
                print(st+'Second preprocessed : ',self.dates[-1])
                continue 

            ret,th1 = cv2.threshold(img_blur, 100, 225, cv2.THRESH_BINARY)
            img_str_3 = pt.image_to_string(Image.fromarray(th1), lang = 'eng',config=config)
            img_str_3 = list(set(map(lambda x : x.strip(), img_str_3.split('\n'))))
            self.find_date(img_str_3)
            if self.dates:
                print(st+'Third preprocessed : ',self.dates[-1])
                continue 

            img_ad_thres = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            img_str_4 = pt.image_to_string(Image.fromarray(img_ad_thres),lang='eng',config=config)
            img_str_4 = list(set(map(lambda x : x.strip(), img_str_4.split('\n'))))
            self.find_date(img_str_4)
            if self.dates:  
                print(st+'Forth preprocessed : ',self.dates[-1])
                continue 
        
        return self.dates

@app.route('/')
def home_direc():
    return "Home Page."

# use to API calls this simply return a dictionary object
@app.route('/extract_date',methods = ['POST'])
def predict_api():
    d = {}
    try:
        # Return list of dictionary data
        data = request.get_json(force=True) 
        if len(data) > 1:
            return jsonify("You are passing more than one image base64 form. Please send only\
                single image base64 form.")
        
        if not len(data):
            return jsonify("You are passing empty base64 form.")
        
        key = list(data[0].keys())[0]
        if key != 'base_64_image_content':
            return jsonify('key is not matched with "base_64_image_content"')
        
        value = list(data[0].values())[0]
        base64_img = value.split(',')
        if len(base64_img) == 1: 
            base64_img = base64_img[0]
        else:
            base64_img = base64_img[1]        
        obj = DateFinder()
        dates = pd.Series(obj.extract_img_str(base64_img))
        if not dates.empty:
            d['date'] = dates.mode()[0]
        else:
            d['date'] = None
    except Exception as e:
        print(e)
        return jsonify("Something went wrong.")

    return jsonify(d)

if __name__ == "__main__":
        app.run(debug=True)