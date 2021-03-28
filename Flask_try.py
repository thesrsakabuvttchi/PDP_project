from flask import request
from flask import Flask,redirect
import requests
import json
from datetime import date

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Get_Token():
    return 'Sucess! You Can close the window'

