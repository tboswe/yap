import click
import os
import requests
import ssl
import webbrowser
import json

from threading import Thread
from time import time, sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
from pathlib import Path
import util

ACCESS_CODE = None
YAHOO_OAUTH_URL = "https://api.login.yahoo.com/oauth2"

with open("creds.json", "r") as read_file:
    data = json.load(read_file)
client_id = data['consumer_key']
client_secret = data['consumer_secret']

def login(client_id, client_secret, redirect_uri, redirect_http, listen_port, persist_key):
    global ACCESS_CODE
    persisted_auth_data = load("auth", default={}, ttl=-1, persist_key=persist_key)
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    url = YAHOO_OAUTH_URL + "/request_auth?" + urlencode(params)
    webbrowser.open_new_tab(url)
    print("Launching OAuth handler server on localhost:{}".format(listen_port))
    server = HTTPServer(("", listen_port), Handler)
    if not redirect_http:
        print("Using localhost SSL certificate (HTTPS)")
        server.socket = ssl.wrap_socket(
            server.socket,
            server_side=True,
            certfile=Path(__file__).parent / "localhost.pem",
            keyfile=Path(__file__).parent / "localhost-key.pem",
            ssl_version=ssl.PROTOCOL_TLS,
        )
    # This will serve until we get a valid access code, then it will shutdown by itself
    server.serve_forever()
    if not ACCESS_CODE:
        error("Couldn't determine access code from URL string", exit=True)
    resp = requests.post(
        YAHOO_OAUTH_URL + "/get_token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": ACCESS_CODE,
            "redirect_uri": "oob",
        },
    )
    try:
        body = resp.json()
        access_token = body.get("access_token")
        access_token_expires = time() + body.get("expires_in")
        refresh_token = body.get("refresh_token")
    except Exception:
        error("Couldn't get access token or refresh token", exit=True)

    persist_file = get_persistence_filename(persist_key)
    success(
        "Access token retrieved!. This will be persisted at {}".format(persist_file)
    )
    save(
        "auth",
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "access_token": access_token,
            "access_token_expires": access_token_expires,
            "refresh_token": refresh_token,
        },
        persist_key=persist_key,
    )
    print("Access Token : {}".format(access_token))
    print("Refresh Token: {}".format(refresh_token))


def shutdown_server(server):
    sleep(0.1)
    server.shutdown()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_CODE
        try:
            access_code = parse_qs(urlparse(self.path).query)["code"][0]
            ACCESS_CODE = access_code
        except Exception:
            print("Couldn't find the access code in the query string....")
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Got it! You may close this tab now".encode())
        thread = Thread(target=shutdown_server, args=(self.server,))
        thread.is_daemon = True
        thread.start()

    def log_message(self, format, *args):
        return