import smtplib
from getpass import getpass
from email.mime.text import MIMEText

sender = 'hasanashqeen@yahoo.com'
receiver = 'hasanashqeen@yahoo.com'

#content = '<a href="http://www.google.com">Wassup kigga</a>'
content = '''
<!DOCTYPE html>
<html>
<head>
<style>

body {
  font-family: "Open Sans", sans-serif;
}
th, td {background: #eee; padding: 8px}

@media screen and (max-width: 600px) {
  table {
    width: 100%;
  }

  table thead {
    display: none;
  }

  table tr, table td {
    border-bottom: 1px solid #ddd;
  }

  table tr {
    margin-bottom: 8px;
  }

  table td {
    display: flex;
  }
}

</style>
</head>
<body>

<table>
  <thead>
    <tr>
      <th>Account</th>
      <th>Due Date</th>
      <th>Amount</th>
      <th>Period</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Visa - 3412</td>
      <td>04/01/2016</td>
      <td>$1,190</td>
      <td>03/01/2016 - 03/31/2016</td>
    </tr>
    <tr>
      <td>Visa - 6076</td>
      <td>03/01/2016</td>
      <td>$2,443</td>
      <td>02/01/2016 - 02/29/2016</td>
    </tr>
    <tr>
      <td>Corporate AMEX</td>
      <td>03/01/2016</td>
      <td>$1,181</td>
      <td>02/01/2016 - 02/29/2016</td>
    </tr>
    <tr>
      <td>Visa - 3412</td>
      <td>02/01/2016</td>
      <td>$842</td>
      <td>01/01/2016 - 01/31/2016</td>
    </tr>
  </tbody>
</table>

</body>
</html>

'''

# One-time password made in Yahoo account
# Only possible after enabling 2-step verification
password = "dyovtnlytudozfsw"

msg = MIMEText(content, 'html')
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = 'First Email with Python'

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
