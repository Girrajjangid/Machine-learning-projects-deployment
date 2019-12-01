# Date Extractor OCR Engine

## Aim: 
1. To build an OCR model that extracts only Expense date from ﬁnancial or any transaction receipts. 
2. Deploy that model on Amazon Web Services as an API.

## Project Structure:
This project has following major parts :

1. _0-6.preprocess.ipynb_ - These files contains all attempts and preprocessing which I used.
2. _all_image_dates.txt_ - Contains dates which manually collected from images.
3. _image_data.csv_ - This file contains original and predicted date.
4. _sample.png_ - Sample image which I going to test.
5. _images.zip_ - Contains all images.
6. _model_LOCAL/api.py_ - This file contains Flask code with modelling.
7. _model_LOCAL/model.py_ - This file used to test on AWS terminal.
8. _model_LOCAL/request.py_ - This file used to send base64 string to Flask API.
9. _model_LOCAL/requirements.txt_ - Contains all required libraries.
10. _model_LOCAL/base64_2.txt_ - Contains base64 form of *sample.png* file

## Sample Image:

We have to extract marked date in **YYYY-MM-DD** format.

![Alt text](https://github.com/Girrajjangid/Machine-learning-projects-deployment/blob/master/03.%20TextExtractor_OCR(Deploy_AWS)/sample.png)

## Let's Start:
### 1. Run on local machine.
*I am assuming you are using Window 10.*

*Run the following commands in terminal.*

```
git clone https://github.com/Girrajjangid/Machine-learning-projects-deployment.git
```

Make sure you are in `Machine-learning-projects-deployment/03. TextExtractor_OCR(Deploy_AWS)/model_LOCAL/` directory.

1. It ensures that you have required libraries.
```
pip install -r requirements.txt
```
2. Extract **images.zip**

3. Finding date by passing image path.
```
python model.py ../sample.png
```
`Expected Output:`
> With (3,3) filter and First preprocessed :  2017-05-09

> With (5,5) filter and First preprocessed :  2017-05-09

> With (7,7) filter and First preprocessed :  2017-05-09

> {'date': '2017-05-09'}

4. It starts Flask API.
```
python api.py
```
This create a WSGI mini server which responsible for communication between web to python.
By default, flask will run on port 5000.

5. Navigate to URL http://127.0.0.1:5000/

You will see something like this:

`Home Page.`


6. Now, We have to send Image in its base64 form. So, To convert any image into its base form click on [This](https://www.base64-image.de/) then click on `show_code` then `copytoclipboard For use in <img> elements:`

You can't access **POST|http://127.0.0.1:5000/extract_date** directly from browser. 

But I can show you two different ways.

6.1. By running new script in new terminal.

```
python request.py
```

`Expected Output:`

> {'date': '2017-05-09'}

6.2. By using [Postman](https://www.getpostman.com/). Postman is a app for interacting with HTTP APIs. It presents you with a friendly GUI for constructing requests and reading responses. 

* Download postman and run it.

* select `POST` method and paste this URL `http://127.0.0.1:5000/extract_date`
Go to the `Body` and then select `raw`

* write payload in this form 

>[{"base_64_image_content" : "<Base64_form>"}]

**For example:**

>[{"base_64_image_content" : "data:image/png;base64,iVBORDzr4--------12AAAA=="}]

`Expected Output:`

![alt text](https://github.com/Girrajjangid/Machine-learning-projects-deployment/blob/master/03.%20TextExtractor_OCR(Deploy_AWS)/utils/1.png)

### 2. Run on AWS Instance.

Amazon Web Services is a subsidiary of Amazon that provides on-demand cloud computing platforms and APIs to individuals, companies, and governments, on a metered pay-as-you-go basis.

Please go through [this](https://aws.amazon.com/ec2/getting-started/) to know more about how to create and run instance on AWS.

1. This is the public URL of instance where I deploy this model http://35.174.170.116:8080/. If you click on this you will see something like this.

`Home Page.`

2. To pass payload to this URL you can use Postman. Which I show above.

If you run Postman and paste this URL http://35.174.170.116:8080/extract_date with `POST` method and hit `send.`
You will see something like this.

![alt text](https://github.com/Girrajjangid/Machine-learning-projects-deployment/blob/master/03.%20TextExtractor_OCR(Deploy_AWS)/utils/2.png)

## Working flow diagram:

![alt text](https://github.com/Girrajjangid/Machine-learning-projects-deployment/blob/master/03.%20TextExtractor_OCR(Deploy_AWS)/utils/3.jpg)







