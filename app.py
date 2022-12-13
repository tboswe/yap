from flask import Flask, redirect, jsonify

app = Flask(__name__)

#YAHOO AUTH FLOW
@app.route('/auth', methods=['GET'])
def get_authorization():
    #this url works to get the user to authorize data access and goes to yap.html with an appended code...not token exchange is done yet
    return redirect("https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj&redirect_uri=https://thebeau.dev/yap/yap.html&response_type=code&language=en-us")

@app.route('/get_token/<redirect_uri>', methods=['GET'])
def get_token():
    #grant_type=authorization_code&redirect_uri=https%3A%2F%2Fwww.example.com&code=abcdef
    #here we'll exchange the code for a token, as described on the yahoo api auth flow.  <code> will come from the auth code appended to the url on the get_authorization redirect
    return None


#get user fantasy information
@app.route('/getuserdata', methods=['GET'])
def get_user_data():
    #'https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nhl/teams'
    #get the user leagues or teams here to give him the choice to select which team he wants to use
    #probably filter out any non fantasy nhl team for now
    #/users;use_login=1/{sub_resource}
    #/users;use_login=1;out={sub_resource_1},{sub_resource_2}
    return None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)