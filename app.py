from flask import Flask, redirect

app = Flask(__name__)

#auth into yahoo
@app.route('/auth', methods=['GET'])
def get_authorization():
    #this url works to get the user to authorize data access and goes to yap.html with an appended code...not token exchange is done yet
    return redirect("https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj&redirect_uri=https://thebeau.ca/yap/yap.html&response_type=code&language=en-us")

@app.route('/token/<code>', methods=['GET'])
def get_token():
    #here we'll exchange the code for a token, as described on the yahoo api auth flow.  <code> will come from the auth code appended to the url on the get_authorization redirect
    return None

#get user fantasy information

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)