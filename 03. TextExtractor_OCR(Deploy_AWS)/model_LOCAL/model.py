import re
import cv2
import sys
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract as pt
from dateutil.parser import parse
pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

class DateFinder():
    
    def __init__(self):
        self.pattern1 = r"(\d{1,4}([.'’~\-/])\d{1,2}([.'’~\-/])\d{1,4})"
        self.pattern2 = r"(\d{1,4}([.'’~\-/\s])[ADFJMNOSadfjmnos]\w*([.'’~\-/\s]*)\d{1,4})"
        self.pattern3 = r"([ADFJMNOSadfjmnos]\w*\s\d{1,4}([,'’~.\-/\s]*)([.'’~\-/\s])\d{1,4})"
        self.pattern4 = r"[ADFJMNOSadfjmnos]\w*\d{1,4}(['’]*)\d{1,4}"
        self.pattern5 = r"(\d{1,4}([.'’~\-/\s])\d{1,4}"
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
                i = i.replace('~',"-")
                i = parse(i).strftime("%Y-%m-%d")
                if 1999 < int(i[:4]) < 2020:
                    self.dates.append(i)   
            except:
                continue
                
    def extract_img_str(self,path):
        config = ("-l eng --oem 1 --psm 3")
        filters = [3,5,7]
        for i in filters:
            st = 'With ({0},{0}) '.format(i) + 'filter and '
            gaussian_filter = (i,i)
            img = cv2.imread(path) 
            img = cv2.resize(img, None, fx = 3, fy = 3, interpolation=cv2.INTER_CUBIC) 
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, gaussian_filter, 0)
            img_str_1 = pt.image_to_string(Image.fromarray(img_blur),lang ="eng",config=config)
            img_str_1 = list(set(map(lambda x : x.strip(), img_str_1.split('\n'))))
            self.find_date(img_str_1)
            if self.dates:
                print(st+'First preprocessed : ',self.dates[-1])
                continue

            img_str_2 = pt.image_to_string(path, lang='eng',config=config)
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

if __name__ == "__main__":
    path  = sys.argv[1]
    obj = DateFinder()
    dates = pd.Series(obj.extract_img_str(path))
    d = {}
    if not dates.empty:
        d['date'] = dates.mode()[0]
    else:
        d['date'] = None
    print(d)