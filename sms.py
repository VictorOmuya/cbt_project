from twilio.rest import Client
import os
import http.client

def get_token():
    
    with open("env.txt", "r") as f:
        return f.read()


    

def sending_sms(number,  mess):
    api_url = 'https://account.kudisms.net/api/'
    username = ''
    password = ''
    sender = 'KudiBrave'
    mobile = number

    conn = http.client.HTTPSConnection("account.kudisms.net")
    payload = ''
    headers = {}
    conn.request("POST", "/api/?username=%s&password=%s&message=%s&sender=%s&mobiles=234%s"%(username, password, mess, sender, mobile),payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    