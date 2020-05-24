import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
now = datetime.datetime.now()
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('your_email','your_password')
from_addr = 'k07224115@gmail.com'
to_addr = "k07224115@gmail.com"
msg = MIMEMultipart()
msg['Subject'] = f"{now.year}.{now.month}.{now.day - 1}"
html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format("target_dataframe".to_html())
part1 = MIMEText(html, 'html')
msg.attach(part1)
smtp.sendmail(from_addr, to_addr, msg.as_string())
smtp.quit()
