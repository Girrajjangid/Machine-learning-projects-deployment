# if you are not use postman to send data then just simple run this file on jupyter_notebook or spyder

import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json=[{'experience':2, 'test_score':9, 'interview_score':6}])

print(r.json())