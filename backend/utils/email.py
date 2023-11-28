import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#create a singleton class for the email client
#check if conn is not None, if it is none --> create a client and authenticate it 
#if not none, use it send an email to the receiver


htmlMessage = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style type="text/css">
      table {
        background: white;
        border-radius:3px;
        border-collapse: collapse;
        height: auto;
        max-width: 900px;
        padding:5px;
        width: 100%;
        animation: float 5s infinite;
      }
      th {
        color:#D5DDE5;;
        background:#1b1e24;
        border-bottom: 4px solid #9ea7af;
        font-size:14px;
        font-weight: 300;
        padding:10px;
        text-align:center;
        vertical-align:middle;
      }
      tr {
        border-top: 1px solid #C1C3D1;
        border-bottom: 1px solid #C1C3D1;
        border-left: 1px solid #C1C3D1;
        color:#666B85;
        font-size:16px;
        font-weight:normal;
      }
      tr:hover td {
        background:#4E5066;
        color:#FFFFFF;
        border-top: 1px solid #22262e;
      }
      td {
        background:#FFFFFF;
        padding:10px;
        text-align:left;
        vertical-align:middle;
        font-weight:300;
        font-size:13px;
        border-right: 1px solid #C1C3D1;
      }
    </style>
  </head>
  <body>
"""


def generate_message(html,toEmail) -> MIMEMultipart:
    message = MIMEMultipart("alternative", None, [MIMEText(html, 'html')])
    message['Subject'] ="Applications status" 
    message['From'] = 'jobtrackersefall23@gmail.com' 
    message['To'] = toEmail
    return message



class Email():
    def __init__(self):
        print("class has been initialized")
        print("starting smtp connection")
        server = smtplib.SMTP('smtp.gmail.com',587) 
        server.ehlo()
        server.starttls()
        print("starting tls connection")
        #email == jobtrackersefall2023@gmail.com 
        #password == j5pTBnzY^-eP
        #apppassword == yhwcmmgtoixdfzkl
        
        server.login("jobtrackersefall2023@gmail.com","yhwcmmgtoixdfzkl")
        self.conn = server

    def send(self,senderEmail,message):
        content = f"{htmlMessage}{message}</body></html>"
        self.conn.sendmail("jobtrackersefall2023@gmail.com",senderEmail,generate_message(content,senderEmail).as_string())


email = Email()
