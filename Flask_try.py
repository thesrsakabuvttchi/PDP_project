from flask import request
from flask import Flask,redirect
import requests
import json
from datetime import date,timedelta


def AddEvent(Title,Time1,Time2):
    Auth = open("Tokens.json")
    Auth = Auth.read()
    Token = json.loads(Auth)['access_token']

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        'authorization': "Bearer "+Token,
        'content-type': "application/json"
    }

    JSON ={
        "summary": Title,
        "start": {
            "dateTime": Time1
        },
        "end": {
            "dateTime": Time2
        }
    }
    x = requests.post(url, headers = headers, data = json.dumps(JSON,indent = 4))

    return(x.text)

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
        'redirect_uri':'https://chronos-api00.herokuapp.com/',
        'grant_type':'authorization_code'
        }

    x = requests.post(url, data = myobj)
    print(x.text)

    of = open("Tokens.json", "w") 
    of.write(x.text)

    return 'Sucess! You Can close the window'

@app.route('/Auth')
def AutoAuth():
    authorization_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=131866851144-bqa6rq5h5kfg4ojnhb3lg2au2mags4ov.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fchronos-api00.herokuapp.com%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.metadata.readonly&state=2E934PToHGBTh4KCPXw2WlU5Nk8QOn&access_type=offline&include_granted_scopes=true"
    return redirect(authorization_url)

@app.route('/Get')
def GetEvents():
    today = str(date.today())
    tomorrow = str(date.today() + timedelta(days=1))

    Auth = open("Tokens.json")
    Auth = Auth.read()
    Token = json.loads(Auth)['access_token']

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        'authorization': "Bearer "+Token,
        'content-type': "application/json"
    }
    params = {
        'timeMin' : today+'T00:00:00+05:30',
        'timeMax' : tomorrow+'T00:00:00+05:30'
    }

    x = requests.get(url,headers =headers,params=params)
    if(x.status_code!=200):
        return None
    Data = json.loads(x.text)['items']

    Events = []
    for i in Data:
        summary = i['summary']
        begin = i['start'][(next(iter(i['start'])))]
        end = i['end'][next(iter(i['end']))]
        Events.append({'Title':summary,'Begin':begin[11:15],'End':end})

    JSON = {'events':Events}
    JSON = json.dumps(JSON, indent = 4)  

    return(JSON)

@app.route('/Add',methods=['GET'])
def CreateEvent():
    Title = request.args.get('Title')
    Time1 = request.args.get('Time1')
    Time2 = request.args.get('Time1')
    print(Title,Time1,Time2)
    return(AddEvent(Title,Time1,Time2))
