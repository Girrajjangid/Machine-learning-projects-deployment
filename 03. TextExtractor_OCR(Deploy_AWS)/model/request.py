import requests

url = 'http://127.0.0.1:5000/extract_date'
with open('base24_2.txt','r') as fl:
    data = fl.read()
r = requests.post(url,json=[{'base_64_image_content':data}])
print(r.json())