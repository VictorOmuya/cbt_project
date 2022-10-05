from twilio.rest import Client
import os

def get_token():
    
    with open("env.txt", "r") as f:
        return f.read()

def send_sms(number, mess):
    num = number
    account_sid = "ACa59320f2dad74cafe284fd22f01f7476"
    auth_tok = os.environ.get("auth_token")
    #auth_token= auth_tok[14:-1]
    
    client = Client(account_sid, auth_tok)

    message = client.messages.create(
    body= mess,
    from_='[+][1][9388882655]',
    to='[+][234][%s]' %num
    )
    #print(message.sid)
    