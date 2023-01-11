from twilio.rest import Client
import os
import http.client

def get_token():
    
    with open("env.txt", "r") as f:
        return f.read()

def send_sms(number, mess):
    num = number
    account_sid = "ACa59320f2dad74cafe284fd22f01f7476"
    auth_tok = "c9c11862eabd0d08cdeb21f145aa7359"
    #auth_token= auth_tok[14:-1]
    
    client = Client(account_sid, auth_tok)

    message = client.messages.create(
    body= mess,
    from_='[+][1][9388882655]',
    to='[+][234][%s]' %num
    )
    #print(message.sid)
    

def sending_sms(number,  mess):
    api_url = 'https://account.kudisms.net/api/'
    username = 'cseantest1@gmail.com'
    password = 'Diamond@2007'
    sender = 'KudiBrave'
    mobile = number

    conn = http.client.HTTPSConnection("account.kudisms.net")
    payload = ''
    headers = {}
    conn.request("POST", "/api/?username=%s&password=%s&message=%s&sender=%s&mobiles=234%s"%(username, password, mess, sender, mobile),payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    