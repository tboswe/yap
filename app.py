from flask import Flask, redirect, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

#YAHOO AUTH FLOW
@app.route('/auth', methods=['GET'])
def get_authorization():
    #this url works to get the user to authorize data access and goes to yap.html with an appended code...not token exchange is done yet
    return redirect("https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj&redirect_uri=https://thebeau.dev/yap/yap.html&response_type=code&language=en-us")

@app.route('/authurl', methods=['GET'])
def get_authurl():
    authurl = {
        'authurl': "https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj&redirect_uri=https://thebeau.dev/yap/yap.html&response_type=code&language=en-us",
        }
    return jsonify(authurl)

@app.route('/appcreds', methods=['GET'])
def get_appcreds():
    creds = {
        'clientid': 'dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj',
        'redirect_uri': 'https://thebeau.dev/yap/yap.html',
        }
    return jsonify(creds)

@app.route('/get_token', methods=['GET'])
def get_token():
    resp = requests.post(
        'https://api.login.yahoo.com/oauth2/' + 'get_token',
        data={
            "client_id": 'dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj',
            "client_secret": '556577b5e9ece81e03edea4f5baf2b0fdfe432e7',
            "grant_type": "authorization_code",
            "code": requests.args.get('code'),
            "redirect_uri": "https://thebeau.dev/yap/yap.html",
        },
    )

    return jsonify(resp.json())
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)