# Machine Learning Engineer Nanodegree
## Capstone Project
Edy Zhang
December 28st, 2017

## Dataset
The dataset used in this project is UCI Machine Learning Repository Cardiotocography Dataset: https://archive.ics.uci.edu/ml/datasets/Cardiotocography#. The original dataset is download to this repo as CTG.xls. A secondary excel spreadsheet, CTG_cleaned.xlsx, was created and used in the ipython notebook. This spreadsheet was created based on the "Raw Data" sheet from the original dataset with the deletion of a few summary and empty rows.

## Notebook
The ipython notebook, notebook.ipython and notebook.html, contains steps using to explore and preprocess the data, as well as training, tuning, and performance compare various classification models. A scaler model, created by sklearn min-max-scaler, is saved as scaler.sav. A classification model, created by tuned sklearn random forest classifier, is saved as forest.sav. The notebook requires python 3+, and the following libraries: numpy, pandas, matplotlib, sklearn, pickle, and keras.

## API code
File predictions.py contains the code for the REST API.

## AWS Setup
The REST API is made publicly available by AWS technologies. The API code was deployed to AWS using Zappa. Zappa helped package the code with necessary libraries, upload package to AWS S3, created AWS Lambda to serve the API, created AWS API Gateway to handle incoming requests, and created the necessary AWS IAM Roles to make S3 contents accessible from API. Two models, scaler.sav and forest.sav, are both uploaded to AWS S3.

## How to Use this API
Please make a POST request to the following URL: https://6p9hezhktb.execute-api.us-west-2.amazonaws.com/prod
The request body needs to include 18 attributes in json format, please refer to below examples. The request will return a prediction in json format, with key of nsp, and value ranges from 1 to 3. 1 means normal, 2 means suspected, and 3 means pathological.

Example body to return 1:
{
"lb":132,
"astv":17,
"ds":0,
"dp":0,
"width":64,
"max":126,
"nmax":2,
"median":121,
"tendency":1,
"ac":0,
"fm":0,
"uc":0,
"mstv":0.5,
"altv":43,
"mltv":2.4,
"dl":0,
"nzeros":0,
"variance":73
}

Example body to return 2:
{
"lb":120,
"astv":73,
"ds":0,
"dp":0,
"width":64,
"max":126,
"nmax":2,
"median":121,
"tendency":1,
"ac":0,
"fm":0,
"uc":0,
"mstv":0.5,
"altv":43,
"mltv":2.4,
"dl":0,
"nzeros":0,
"variance":73
}

Example body to return 3:
{
"lb":134,
"astv":26,
"ds":0,
"dp":2,
"width":150,
"max":200,
"nmax":6,
"median":107,
"tendency":0,
"ac":1,
"fm":0,
"uc":10,
"mstv":5.9,
"altv":43,
"mltv":2.4,
"dl":0,
"nzeros":0,
"variance":73
}
