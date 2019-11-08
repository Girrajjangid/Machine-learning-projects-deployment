# Deep Convolutional Neural Network model for Animal Classification.

In this project we deploy animal classification model as a flask API.

**Note:** 
- It's always better to write model and API code in different files.
- It's better to see ***requirements.txt*** file before running them.
- Ensure that you are in the project home directory.

## Project Structure
This project has two major parts :
1. _animal_classifier.py_ - This file contain Model training.
2. _api.py_ - This contains Flask code that receive image through GUI.


## Steps to run the project.

1. It ensures that you have required libraries installed-
```
pip install -r requirements.txt
```

2. It creates the model-
```
python _animal_classifier.py
```
Expected Output:

> Model Created.

`
	+---------+
    | ConvNet |
    +---------+------------------+
    | Input Shape: (200, 200, 3) |
	-----------------------------+
	_________________________________________________________________________
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
	|	 	                                                                |
	| Total params: 5,088,666                                               |
	| Trainable params: 5,051,802                                           |
	| Non-trainable params: 36,864                                          |
	|_______________________________________________________________________|
`

> Training starts...

> Model Successfully Saved.

This would create a serialized file of our model as `model.h5`

3. Run api.py using below command to start Flask API
```
python api.py
```

This create a WSGI mini server which responsible for communication between web to python.
By default, flask will run on port 5000.

4. Navigate to URL http://localhost:5000/
You will see something like this:

![alt text](http://assets/8.png)

Select image from `uploads` folder.

![alt text](http://assets/9.png)

![alt text](http://assets/10.png)

Click on `Predict`.
![alt text](http://assets/11.png)

DONE!!

## Model Architecture

![alt text](http://assets/2.png)

#### [Download Dataset from here](https://www.kaggle.com/alessiocorrado99/animals10)
