import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# return prediction on web page
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    try:
        int_features = [int(x) for x in request.form.values()] # this is generator extract all values from web
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
    except:
        return render_template('index.html', prediction_text="Something went wrong.")
     
    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be Rs. {}'.format(output))

# use to API calls
# this simply return a dictionary object
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls throught request
    '''
    try:
        data = request.get_json(force=True)
        pred = []
        for each in data:
            prediction = model.predict([np.array(list(each.values()))])
            pred.append(prediction[0])
    except:
        return jsonify('something went wrong')

    return jsonify(pred)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)