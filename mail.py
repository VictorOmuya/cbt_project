import smtplib

gmail_user = 'adavizeadebisi@gmail.com'
gmail_password = 'pythonmailing'
sub = 'Your One Time Pass'

def mail_otp(address, number):
    
    sent_from = gmail_user
    to = [address]
    subject = sub
    body = 'Your One Time Password is: ', number

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    #try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()   
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
    #except:
        #print ('Something went wrong...')
        
    
#mail_otp('victor_zik@yahoo.com', 533456)
