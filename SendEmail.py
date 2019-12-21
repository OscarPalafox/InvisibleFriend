from smtplib import SMTP_SSL
from datetime import datetime
from textwrap import dedent
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# Credentials of the email account
gmail_user = "regalosfamiliapalafox@gmail.com"
gmail_password = "Gascons1"

# Log in the gmail server
server = SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)

# Fetch current date
current = datetime.now()


def send_email(receiver, gifted):
    email = MIMEMultipart()
    email['From'] = 'Regalos Navidad'
    email['To'] = receiver
    email['Subject'] = f"Regalo invisible para el {current.year + 1}"

    # The body_email.txt can be changed to anything, just be sure to include the variable {0} in the body
    body = open("body_email.txt", "r").read().format(gifted)

    email.attach(MIMEText(body, 'plain'))

    email_text = email.as_string()

    server.sendmail(gmail_user, receiver, email_text.encode('utf-8'))
