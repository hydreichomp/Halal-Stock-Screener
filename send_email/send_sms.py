import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "hasanashqeen@yahoo.com"
pas = "dyovtnlytudozfsw"

sms_gateway = '8175648002@tmomail.net'
smtp = "smtp.mail.yahoo.com"
port = '587'

# This will start our email server
server = smtplib.SMTP(smtp, port)
# Starting the server
server.starttls()
# Logging into the server
server.login(email, pas)

# Now we use the MIME module to structure our message
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = sms_gateway
# Make sure you add a new time in the subject
msg['Subject'] = "Sent through Python\n"
# Make sure you add new lines to your body
body = "sup sand kigga\n"
# and then attach that body furthermore you can also send html content
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email, sms_gateway, sms)

# Lastly, quit the server
server.quit()
