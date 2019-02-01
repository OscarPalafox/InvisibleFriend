import smtplib
import datetime

# Credentials of the email account
gmail_user = ""  
gmail_password = ""

# Log in the gmail server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)

# Fetch current date
current = datetime.datetime.now()


def send_email(receiver, gifted):
	subject = "Regalo invisible para el %s" % (current.year + 1)
	
	# The body can be changed to anything, just be sure to include the variable gifted
	body = """Hoooola,
Espero que estés pasando unas geniales navidades. Como sé que cada año se nos olvida quién nos toca el año que viene te mando un email para que no se te olvide :)
La persona que te ha tocado es: %s
Que vaya todo muy bien y que tengas próspero año nuevo :)

Besos""" % (gifted)

	email_text = """  
To: %s  
Subject: %s

%s
""" % (receiver, subject, body)

	server.sendmail(gmail_user, receiver, email_text.encode('utf-8'))