from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

model_pickle = open("./classifier.pkl", "rb")
clf = pickle.load(model_pickle)

#First sample Endpoint
@app.route("/ping", methods=['GET'])
def ping():
    return {"message": "This is Network Anomaly Prediction Application!!"}


@app.route("/predict", methods = ["POST", "GET"])

def prediction(network_anomaly):
    # Pre-processing user input
#     anomaly = request.get_json()
    print(network_anomaly)

    if network_anomaly['protocoltype'] == "tcp":
        protocoltype = 1
    elif network_anomaly['protocoltype'] == "udp":
        protocoltype = 2
    else:
        protocoltype = 3

    srcbytes = network_anomaly['srcbytes']
    dstbytes = network_anomaly['dstbytes']
    wrongfragment = network_anomaly['wrongfragment']
    loggedin = network_anomaly['loggedin']
    count = network_anomaly['count']
    dsthostsrvcount = network_anomaly['dsthostsrvcount']
    lastflag = network_anomaly['lastflag']

    # Making predictions
    prediction = clf.predict([[protocoltype, srcbytes, dstbytes, wrongfragment, loggedin, count, dsthostsrvcount, lastflag]])

    if prediction == 0:
        pred = "Normal"
    else: 
        pred = "Anomolous"
        
    return pred


#Endpoint to get template request for model inferance
#@app.route("/template",methods = ['GET'])
#  def get_template():
#     return  {
#      'protocoltype': 1,
#     'srcbytes': 495,
#     'dstbytes': 8155,
#     'wrongfragment': 3,
#     'loggedin': 0,
#     'count' : 412,
#     'dsthostsrvcount' : 213,
#     'lastflag' : 20
# }