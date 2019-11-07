## DL model Animal Classifier
In this project we animal classification model as a flask API.

Ensure that you are in the project home directory.
Run this command into terminal. It ensures that you have the correct libraries. It's better to see requirements.txt file.
### Steps to run the project:
1. 
```
pip install -r requirements.txt
```

2. Create the machine learning model by running below command -
```
python model.py
```
Expected Output ```Model Saved Successfully.```
This would create a serialized file of our model as model.pkl


3. Run api.py using below command to start Flask API
```
python api.py
```
It's always better to write model and API code in different files.
This create a WSGI mini server which responsible for communication between web to python.
By default, flask will run on port 5000.

5. Navigate to URL http://localhost:5000/
Now you will see something like this:

![alt text](http://www.thepythonblog.com/wp-content/uploads/2019/02/Homepage.png)

Enter valid numerical values in all 3 input boxes and hit Predict.

If everything goes well, you should  be able to see the predcited salary vaule on the HTML page!
![alt text](http://www.thepythonblog.com/wp-content/uploads/2019/02/Result.png)

4. You can also send direct POST requests to FLask API using Python's inbuilt request module
Run the beow command to send the request with some pre-popuated values -
```
python request.py
```



    +---------+
    | ConvNet |
    +---------+
    Input Shape: (200, 200, 3)
_________________________________________________________________
|      Layer (type)              |   Output Shape        |    Param #   |
|================================|=======================|==============|
| conv2d (Conv2D)                | (None, 200, 200, 16)  |    448       |
|________________________________|_______________________|______________|
| conv2d_1 (Conv2D)              | (None, 200, 200, 16)  |    2320      |
|________________________________|_______________________|______________|
| max_pooling2d (MaxPooling2D)   | (None, 100, 100, 16)  |    0         |
|________________________________|_______________________|______________|
| conv2d_2 (Conv2D)              | (None, 100, 100, 32)  |    4640      |
|________________________________|_______________________|______________|
| conv2d_3 (Conv2D)              | (None, 100, 100, 32)  |    9248      |
|________________________________|_______________________|______________|
| max_pooling2d_1 (MaxPooling2D) | (None, 50, 50, 32)    |    0         |
|________________________________|_______________________|______________|
| conv2d_4 (Conv2D)              | (None, 50, 50, 64)    |    18496     |
|________________________________|_______________________|______________|
| conv2d_5 (Conv2D)              | (None, 50, 50, 64)    |    36928     |
|________________________________|_______________________|______________|
| max_pooling2d_2 (MaxPooling2D) | (None, 25, 25, 64)    |    0         |
|________________________________|_______________________|______________|
| conv2d_6 (Conv2D)              | (None, 25, 25, 128)   |    73856     |
|________________________________|_______________________|______________|
| conv2d_7 (Conv2D)              | (None, 25, 25, 128)   |    147584    |
|________________________________|_______________________|______________|
| max_pooling2d_3 (MaxPooling2D) | (None, 12, 12, 128)   |    0         |
|________________________________|_______________________|______________|
| flatten (Flatten)              | (None, 18432)         |    0         |
|________________________________|_______________________|______________|
| batch_normalization_v1 (Batch  | (None, 18432)         |    73728     |
|________________________________|_______________________|______________|
| dense (Dense)                  | (None, 256)           |    4718848   |
|________________________________|_______________________|______________|
| dense_1 (Dense)                | (None, 10)            |    2570      |
|================================|=======================|==============|

Total params: 5,088,666
Trainable params: 5,051,802
Non-trainable params: 36,864
________________________________________________________________________

[Download Dataset from here](https://www.kaggle.com/alessiocorrado99/animals10)
