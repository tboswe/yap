from flask import Flask

app = Flask(__name__)

@app.route("/")
def login():
    #this url works to get the user to authorize data access and goes to yap.html with an appended code...not token exchange is done yet
    url="https://api.login.yahoo.com/oauth2/request_auth?client_id=dj0yJmk9bVJqTU1ob1F0WEpnJmQ9WVdrOVMwSkVia05RVEVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTZj&redirect_uri=https://thebeau.ca/yap/yap.html&response_type=code&language=en-us"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)