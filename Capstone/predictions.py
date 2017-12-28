from flask import Flask
from flask import request
from flask import json
from numpy import log
from pickle import load
from numbers import Number
import boto3

BUCKET_NAME = 'edycoco'
FOLDER_IN_S3 = 'ML/'
MODEL_FILE_NAME = 'forest.sav'
SCALER_FILE_NAME = 'scaler.sav'
TEMP_FOLDER = '/tmp/'

app = Flask(__name__)

## request handler
@app.route('/', methods=['POST'])
def index():
    ## handle invalid requests
    try:
        payload = json.loads(request.get_data().decode('utf-8'))
        if not validate_payload(payload):
            return json.dumps(errormsg()), 400
    except:
        return json.dumps(errormsg()), 400

    ## predict based on input params
    prediction = predict(payload)
    return json.dumps({"nsp": str(prediction[0])})

def validate_payload(payload):
    expecting_keys = ["lb","astv","ds","dp","width","max","nmax","median","tendency","ac","fm","uc","mstv","altv","mltv","dl","nzeros","variance"]
    for key in expecting_keys:
        if key not in payload:
            return False
        elif not isinstance(payload[key], Number):
            return False
    return True

def errormsg():
    return {"error":"payload not in expected format","example":"{\"lb\":120,\"astv\":73,\"ds\":0,\"dp\":0,\"width\":64,\"max\":126,\"nmax\":2,\"median\":121,\"tendency\":1,\"ac\":0,\"fm\":0,\"uc\":0,\"mstv\":0.5,\"altv\":43,\"mltv\":2.4,\"dl\":0,\"nzeros\":0,\"variance\":73}"}

## model stored in s3, retrieved by boto3
def load_model(keyname):
    s3_client = boto3.client('s3')
    s3_client.download_file('edycoco', FOLDER_IN_S3+keyname, TEMP_FOLDER+keyname)
    return load(open(TEMP_FOLDER+keyname, 'rb'))

def predict(data):
    final_data = clean(data)
    return load_model(MODEL_FILE_NAME).predict(final_data)

def clean(data):
    ## log transform
    data = logTrans(data)
    ## scale
    dataCleaned = scale(data)
    return dataCleaned

## same log transformation used at data cleaning before model creation
def logTrans(data):
    cols = ['ac','fm','uc','mstv','altv','mltv','dl','nzeros','variance']
    for col in cols:
        data[col] = log(data[col] + 0.01)
    return data

def scale(data):
    array = []
    array.append(data['lb'])
    array.append(data['astv'])
    array.append(data['ds'])
    array.append(data['dp'])
    array.append(data['width'])
    array.append(data['max'])
    array.append(data['nmax'])
    array.append(data['median'])
    array.append(data['tendency'])
    array.append(data['ac'])
    array.append(data['fm'])
    array.append(data['uc'])
    array.append(data['mstv'])
    array.append(data['altv'])
    array.append(data['mltv'])
    array.append(data['dl'])
    array.append(data['nzeros'])
    array.append(data['variance'])
    array2d = [array]

    return load_model(SCALER_FILE_NAME).transform(array2d)
