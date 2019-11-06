import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# Define a flask app
app = Flask(__name__)

labels_name = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep','spider','squirrel']

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.	dirname(__file__)
        file_path = os.path.join(basepath, 'uploads/', secure_filename(f.filename))
        f.save(file_path)
        
        img = image.load_img(file_path, target_size=(200, 200))
        x = image.img_to_array(img)  # (200,200,3)
        x = np.expand_dims(x, axis=0) # (1,200,200,3)
        
        model = load_model('model.h5')
        model._make_predict_function()    # It create a function to run on GPU
       
        preds = model.predict(x) 
        name  = labels_name[preds.argmax()]
        return name 
    return 'None'

if __name__ == '__main__':
    app.run(debug=True)


