from flask import Flask, redirect, jsonify, request, json, f, render_template
from flask_cors import CORS, cross_origin

import os, time
from rauth import OAuth2Service

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/yap")
def yap():
    return render_template("yap")

@app.route('/yahoo_auth', methods=['GET'])
def get_token():
    #grab params
    f = open('creds.json')
    creds = json.load(f)
    auth_code = request.args.get('auth_code')

    #initialize stuff
    self = object
    self.Token()
    self.oauth = self.oauth = OAuth2Service(
            client_id=creds['consumer_key'],
            client_secret=creds['consumer_secret'],
            name="yahoo",
            authorize_url="https://api.login.yahoo.com/oauth2/request_auth",
            access_token_url="https://api.login.yahoo.com/oauth2/get_token",
            base_url="https://fantasysports.yahooapis.com",
        )
    self.session = None
    #try for token
    self.token.get(self.oauth, auth_code)
    if self.session:
        self.session.access_token = self.otken.access_token

    self.session = self.oauth.get_session(self.token.access_token)
    self.last_request = time.time()
    self.request_period = 0

    return self

@app.route('/auth', methods=['GET'])
def test_auth():
    f = open('creds.json')
    creds = json.load(f)
    redirect f'https://api.login.yahoo.com/oauth2/request_auth?client_id={creds['consumer_key']}&redirect_uri=https://thebeau.dev/yap/yap.html&response_type=code&language=en-us'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

class Token(object):
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiration_time = 0

    @property
    def expires_in(self):
        return self.expiration_time - time.time()

    @property
    def is_expired(self):
        return self.expires_in <= 0

    def get(self, oauth_service, auth_code):
        if self.refresh_token:
            data = {
                "refresh_token": self.refresh_token,
                "redirect_uri": "https://thebeau.dev/yap/yap.html",
                "grant_type": "refresh_token",
            }
        else:
            data = {
                "code": auth_code,
                "redirect_uri": "https://thebeau.dev/yap/yap.html",
                "grant_type": "authorization_code",
            }

        self._get_token(oauth_service, data)

    def _get_token(self, oauth_service, data):
        raw_token = oauth_service.get_raw_access_token(data=data)

        parsed_token = raw_token.json()
        self.access_token = parsed_token["access_token"]
        self.refresh_token = parsed_token["refresh_token"]
        self.expiration_time = time.time() + parsed_token["expires_in"]