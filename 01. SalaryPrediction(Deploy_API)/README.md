## ML-Model-Flask-Deployment

In this project we deploy salary prediction model as a flask API.

### Project Structure
This project has four major parts :
1. _model.py_ - This file contain Modelling.
2. _app.py_ - This contains Flask APIs that receives employee details through GUI or API calls.
3. _request.py_ - This file used to test API.
4. _templates_ - This folder contains the HTML template to allow user to enter employee detail and displays the predicted employee salary.


### Steps to run the project.

### Prerequisites
Ensure that you are in the project home directory.
Run this command into terminal. It ensures that you have the correct libraries. It's better to see requirements.txt file.

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
