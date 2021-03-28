from flask import request
from flask import Flask,redirect
import requests
import json
from datetime import date

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Get_Token():
    code = request.args.get('code')
    print("CODE:",code)

    url = 'https://accounts.google.com/o/oauth2/token'

    myobj = {
        'code': code,
        'client_id':"131866851144-bqa6rq5h5kfg4ojnhb3lg2au2mags4ov.apps.googleusercontent.com",
        'client_secret':"Ba3wZXev9TM5aiyAhFZGXDBL",
        'redirect_uri':'http://192.168.1.3.xip.io:8080/',
        'grant_type':'authorization_code'
        }

    x = requests.post(url, data = myobj)
    print(x.text)

    of = open("Tokens.json", "w") 
    of.write(x.text)

    return 'Sucess! You Can close the window'

