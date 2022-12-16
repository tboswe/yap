from flask import Flask, redirect, jsonify, request, json
from flask_cors import CORS, cross_origin

import os, time
from rauth import OAuth2Service

app = Flask(__name__)
cors = CORS(app, resources={r"/get_key": {'origins': '*'}})

#YAHOO AUTH FLOW
@app.route('/get_key', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_key():
    f = open('creds.json')
    creds = json.load(f)
    #return creds['consumer_key']
    return creds['consumer_key']

@app.route('/get_token', methods=['GET'])
def get_token():
    f = open('creds.json')
    creds = json.load(f)
    auth_code = request.args.get('auth_code')
    return auth_code

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)