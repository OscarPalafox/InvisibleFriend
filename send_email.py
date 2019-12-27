from smtplib import SMTP_SSL
from datetime import datetime
from textwrap import dedent
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from sys import argv


def create_server():
    # Credentials of the email account
    gmail_user = open('user.txt', 'r', encoding='utf-8').read()
    gmail_password = open('credentials.txt', 'r', encoding='utf-8').read()

    # Log in the gmail server
    server = SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    return gmail_user, gmail_password, server


def send_email_gift(gmail_user, gmail_password, server, receiver, gifted, gifter=''):
    # Fetch current date
    current_date = datetime.now()

    email = MIMEMultipart()
    email['From'] = 'Regalos Navidad'
    email['To'] = receiver
    email['Subject'] = f'Regalo invisible para el {current_date.year + 1}'

    # The body_email.txt can be changed to anything, just be sure to include the variable {0} in the body
    gifter = gifter if not gifter else ' ' + gifter
    body = open('body_email.txt', 'r',
                encoding='utf-8').read().format(gifter, gifted)

    email.attach(MIMEText(body))

    email_text = email.as_string()

    server.sendmail(gmail_user, receiver, email_text.encode('utf-8'))


if __name__ == '__main__':
    gmail_user, gmail_password, server = create_server()
    send_email_gift(gmail_user, gmail_password, server, argv[1], argv[2])
    print('Sent successfully!')
