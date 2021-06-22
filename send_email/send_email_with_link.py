import smtplib
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = 'hasanashqeen@yahoo.com'
receiver = 'hasanashqeen@yahoo.com'

# One-time password made in Yahoo account
# Only possible after enabling 2-step verification
password = "dyovtnlytudozfsw"

msg = MIMEMultipart('alternative')
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = 'First Email with Python'

content = '<a href="http://www.google.com">Wassup kigga</a>'
html_body = MIMEText(content, 'html')
msg.attach(html_body)

smtp_server_name = 'smtp.mail.yahoo.com'
port = '587'

if port == '465':
   server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
else:
   server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
   server.starttls() # This is for secure reason

server.login(sender, password)
server.send_message(msg)
server.quit()
